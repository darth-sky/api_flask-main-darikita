"""Routes for module donation_projects"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

donation_projects_endpoints = Blueprint('donation_projects', __name__)
UPLOAD_FOLDER = "img"


@donation_projects_endpoints.route('/read', methods=['GET'])
@jwt_required()
def read():
    """Routes for module get list donation_projects"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = """SELECT donation_project_id, title, description, target_amount, project_photo, current_amount, status, users.name, donation_categories.name as category FROM donation_projects
INNER JOIN users ON donation_projects.user_id = users.user_id
INNER JOIN donation_categories ON donation_projects.category_id = donation_categories.category_id;"""
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@donation_projects_endpoints.route('/readDonated/<int:donation_project_id>', methods=['GET'])
@jwt_required()
def readDonated(donation_project_id):
    """Routes for module get list donation_projects"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = """SELECT d.donation_id, d.donation_project_id, u.name AS user_name, d.amount, d.donated_at
                    FROM donations d
                    JOIN users u ON d.user_id = u.user_id
                    WHERE d.donation_project_id = %s
                    ORDER BY d.donated_at DESC;
                    """
    cursor.execute(select_query, (donation_project_id,))
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@donation_projects_endpoints.route('/readByID/<int:donation_project_id>', methods=['GET'])
@jwt_required()
def read_by_id(donation_project_id):
    """Route to get a single donation project by its ID"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        select_query = """
        SELECT donation_project_id, title, description, target_amount, project_photo, 
               current_amount, status, users.name AS user_name, 
               donation_categories.name AS category 
        FROM donation_projects
        INNER JOIN users ON donation_projects.user_id = users.user_id
        INNER JOIN donation_categories ON donation_projects.category_id = donation_categories.category_id
        WHERE donation_project_id = %s;
        """

        cursor.execute(select_query, (donation_project_id,))
        result = cursor.fetchone()  # Fetch only one record

        cursor.close()
        connection.close()

        if result:
            return jsonify({"message": "OK", "data": result}), 200
        else:
            return jsonify({"message": "Donation project not found"}), 404

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@donation_projects_endpoints.route('/readByUserID/<user_id>', methods=['GET'])
@jwt_required()
def readByUserID(user_id):
    """Routes for module get list donation_projects by user_id"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query untuk mengambil proyek donasi berdasarkan user_id
    select_query = """SELECT donation_project_id, title, description, target_amount, project_photo, current_amount, status, users.name, donation_categories.name as category 
                      FROM donation_projects
                      INNER JOIN users ON donation_projects.user_id = users.user_id
                      INNER JOIN donation_categories ON donation_projects.category_id = donation_categories.category_id
                      WHERE users.user_id = %s;"""
    
    try:
        cursor.execute(select_query, (user_id,))  # Pastikan user_id dipasangkan dengan parameter
        results = cursor.fetchall()
        cursor.close()  # Jangan lupa menutup cursor
        
        if results:
            return jsonify({"message": "OK", "datas": results}), 200
        else:
            return jsonify({"message": "No projects found for this user.", "datas": []}), 200

    except Exception as e:
        cursor.close()
        return jsonify({"message": "Error", "error": str(e)}), 500


# @donation_projects_endpoints.route('/read', methods=['GET'])
# @jwt_required()
# def read():
#     """Routes for module get list donation_projects with optional category filter"""
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     # Get 'category_id' from query parameters
#     category_id = request.args.get('category_id', None)

#     # Base query
#     select_query = "SELECT * FROM donation_projects"

#     # Add filtering condition if category_id is provided
#     if category_id:
#         select_query += " WHERE category_id = %s"
#         cursor.execute(select_query, (category_id,))
#     else:
#         cursor.execute(select_query)

#     # Fetch results
#     results = cursor.fetchall()
#     cursor.close()  # Close the cursor after query execution

#     # Return the response
#     return jsonify({"message": "OK", "datas": results}), 200




@donation_projects_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create():
    """Routes for module create a donation_projects"""
    required = get_form_data(["title"])  # use only if the field required
    title = required["title"]
    description = request.form['description']
    target_amount = request.form['target_amount']
    # project_photo = request.form['project_photo']
    category_id = request.form['category_id']
    user_id = request.form['user_id']

    uploaded_file = request.files.get('project_photo')
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        project_photo = uploaded_file.filename
    else:
        project_photo = 'default.jpg'  


    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO donation_projects (title, description, target_amount, project_photo, user_id, category_id) VALUES (%s, %s, %s, %s, %s, %s)"
    request_insert = (title, description, target_amount, project_photo, user_id, category_id)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    cursor.close()
    new_id = cursor.lastrowid  # Get the newly inserted book's ID\
    if new_id:
        return jsonify({"title": title, "message": "Inserted", "id_donation_projects": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@donation_projects_endpoints.route('/update/<donation_project_id>', methods=['PUT'])
@jwt_required()
def update(donation_project_id):
    """Routes for module update a donation project"""
    # Retrieve data from the request
    title = request.form.get('title')
    description = request.form.get('description')
    target_amount = request.form.get('target_amount')
    category_id = request.form.get('category_id')
    uploaded_file = request.files.get('project_photo')

    # Prepare fields to update dynamically
    fields = []
    values = []

    if title:
        fields.append("title = %s")
        values.append(title)

    if description:
        fields.append("description = %s")
        values.append(description)

    if target_amount:
        fields.append("target_amount = %s")
        values.append(target_amount)

    if category_id:
        fields.append("category_id = %s")
        values.append(category_id)

    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        fields.append("project_photo = %s")
        values.append(uploaded_file.filename)

    # Ensure there are fields to update
    if fields:
        values.append(donation_project_id)
        connection = get_connection()
        cursor = connection.cursor()

        update_query = f"UPDATE donation_projects SET {', '.join(fields)} WHERE donation_project_id = %s"
        cursor.execute(update_query, values)

        if cursor.rowcount <= 0:
            return jsonify({"message": "Data not found"}), 400

        connection.commit()
        cursor.close()

        return jsonify({"message": "updated", "id_donation_projects": donation_project_id}), 200

    return jsonify({"message": "No fields to update"}), 400



# @donation_projects_endpoints.route('/update/<donation_project_id>', methods=['PUT'])
# @jwt_required()
# def update(donation_project_id):
#     """Routes for module update a book"""
#     title = request.form['title']
#     description = request.form['description']
#     target_amount = request.form['target_amount']
#     project_photo = request.files['project_photo']
#     category_id = request.form['category_id']
    
#     uploaded_file = request.files.get('project_photo')
#     if uploaded_file and uploaded_file.filename != '':
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
#         uploaded_file.save(file_path)
#         project_photo = uploaded_file.filename
#     else:
#         project_photo = 'default.jpg'  

#     connection = get_connection()
#     cursor = connection.cursor()

#     update_query = "UPDATE donation_projects SET title=%s, description=%s, target_amount=%s, project_photo=%s, category_id=%s WHERE donation_project_id=%s"
#     update_request = (title, description, target_amount, project_photo, category_id, donation_project_id)
#     cursor.execute(update_query, update_request)
#     if cursor.rowcount <= 0:
#         return jsonify({"message": "Data not found"}), 400
#     connection.commit()
#     cursor.close()
#     data = {"message": "updated", "id_donation_projects": donation_project_id}
#     return jsonify(data), 200


@donation_projects_endpoints.route('/delete/<donation_project_id>', methods=['DELETE'])
@jwt_required()
def delete(donation_project_id):
    """Routes for module to delete a donation project"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM donation_projects WHERE donation_project_id = %s"
    delete_id = (donation_project_id,)  # Perhatikan tanda koma di akhir untuk membuatnya menjadi tuple
    cursor.execute(delete_query, delete_id)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Data deleted", "id_donation_projects": donation_project_id}
    return jsonify(data), 200

# @donation_projects_endpoints.route('/delete/<donation_project_id>', methods=['DELETE'])
# @jwt_required()
# def delete(donation_project_id):
#     """Routes for module to delete a book"""
#     connection = get_connection()
#     cursor = connection.cursor()

#     delete_query = "DELETE FROM donation_projects WHERE donation_project_id = %s"
#     delete_id = (donation_project_id)
#     cursor.execute(delete_query, delete_id)
#     if cursor.rowcount <= 0:
#         return jsonify({"message": "Data not found"}), 400
#     connection.commit()
#     cursor.close()
#     data = {"message": "Data deleted", "id_donation_projects": donation_project_id}
#     return jsonify(data)

@donation_projects_endpoints.route('/approve/<donation_project_id>', methods=['PUT'])
@jwt_required()
def approve(donation_project_id):
    """API to approve a donation project and update its status to 'approved'"""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status to 'approved'
    update_query = "UPDATE donation_projects SET status=%s WHERE donation_project_id=%s"
    update_request = ('approved', donation_project_id)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found or status already approved"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Status updated to approved", "id_donation_projects": donation_project_id}
    return jsonify(data), 200

@donation_projects_endpoints.route('/reject/<donation_project_id>', methods=['PUT'])
@jwt_required()
def reject(donation_project_id):
    """API to reject a donation project and update its status to 'rejected'"""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status to 'rejected'
    update_query = "UPDATE donation_projects SET status=%s WHERE donation_project_id=%s"
    update_request = ('rejected', donation_project_id)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found or status already rejected"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Status updated to rejected", "id_donation_projects": donation_project_id}
    return jsonify(data), 200




@donation_projects_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't upload data"}), 400


@donation_projects_endpoints.route('/donate', methods=['POST'])
@jwt_required()
def donate():
    """Routes for module donate"""        
    donation_project_id = request.form['donation_project_id']
    user_id = request.form['user_id']
    amount = request.form['amount']


    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO donations (donation_project_id, user_id, amount) VALUES (%s, %s, %s)"
    request_insert = (donation_project_id, user_id, amount)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    cursor.close()    
    return jsonify({"donation_project_id": donation_project_id, "user_id": user_id, "amount": amount}), 201    

@donation_projects_endpoints.route('/createKomen/<donation_project_id>', methods=['POST'])
@jwt_required()
def komen(donation_project_id):
    """Routes for module create a book"""
    user_id = request.form["user_id"]
    comment = request.form["comment"]
    print(user_id, comment)
    

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO donation_comments (donation_project_id, user_id, comment) VALUES (%s, %s, %s)"
    request_insert = (donation_project_id, user_id, comment)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    cursor.close()
    connection.close()
    new_id = cursor.lastrowid  # Get the newly inserted book's ID\
    if new_id:
        return jsonify({"comment_id": new_id, "message": "Inserted"}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@donation_projects_endpoints.route('/readKomen/<donation_project_id>', methods=['GET'])
@jwt_required()
def read_komen_with_user_name(donation_project_id):
    """Route to read comments for a specific donation project along with user names"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)  # Enable dictionary mode for better readability

    try:
        # Query to fetch comments and user names for a specific donation project
        query = """
            SELECT 
                dc.comment_id, 
                dc.donation_project_id, 
                dc.user_id, 
                u.name AS user_name,  -- Fetch user name from users table
                dc.comment, 
                dc.commented_at 
            FROM 
                donation_comments dc
            INNER JOIN 
                users u ON dc.user_id = u.user_id  -- Join with users table
            WHERE 
                dc.donation_project_id = %s
            ORDER BY 
                dc.commented_at DESC
        """
        cursor.execute(query, (donation_project_id,))
        comments = cursor.fetchall()

        # Return comments as JSON
        return jsonify({"comments": comments}), 200
    except Exception as e:
        print(f"Error reading comments: {e}")
        return jsonify({"message": "Failed to fetch comments", "error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

