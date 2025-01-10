"""Routes for module volunteer_projects"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

volunteer_projects_endpoints = Blueprint('volunteer_projects', __name__)
UPLOAD_FOLDER = "img"


@volunteer_projects_endpoints.route('/read', methods=['GET'])
@jwt_required()
def read():
    """Routes for module get list volunteer_projects"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = """SELECT volunteer_project_id, title, description, target_amount, project_photo, current_amount, status, users.name, date_started 
                        FROM volunteer_projects INNER JOIN users ON volunteer_projects.user_id = users.user_id;"""
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

@volunteer_projects_endpoints.route('/readVolunteers', methods=['GET'])
@jwt_required()
def readVolunteers():
    """Routes for module get list blood_donation_projects"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = """SELECT volunteer_id, volunteer_projects.title, users.name, deskripsi, volunteers.status, volunteer_projects.volunteer_project_id, volunteers.umur
                        FROM volunteers
                        INNER JOIN volunteer_projects ON volunteers.volunteer_project_id = volunteer_projects.volunteer_project_id
                        INNER JOIN users ON volunteers.user_id = users.user_id;"""
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@volunteer_projects_endpoints.route('/readVolunteered/<int:volunteer_project_id>', methods=['GET'])
@jwt_required()
def readVolunteered(volunteer_project_id):
    """Routes for module get list volunteer_projects"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = """SELECT d.volunteer_id, d.volunteer_project_id, u.name AS user_name, d.deskripsi, d.status, d.joined_at, d.umur
                        FROM volunteers d
                        JOIN users u ON d.user_id = u.user_id
                        WHERE d.volunteer_project_id = %s
                        ORDER BY d.joined_at DESC;
                    """
    cursor.execute(select_query, (volunteer_project_id,))
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

@volunteer_projects_endpoints.route('/readByID/<int:volunteer_project_id>', methods=['GET'])
@jwt_required()
def read_by_id(volunteer_project_id):
    """Route to get a single donation project by its ID"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        select_query = """
        SELECT volunteer_project_id, title, description, target_amount, project_photo, current_amount, status, users.name, date_started
        FROM volunteer_projects INNER JOIN users ON volunteer_projects.user_id = users.user_id
        WHERE volunteer_project_id = %s;
        """

        cursor.execute(select_query, (volunteer_project_id,))
        result = cursor.fetchone()  # Fetch only one record

        cursor.close()

        if result:
            return jsonify({"message": "OK", "data": result}), 200
        else:
            return jsonify({"message": "Donation project not found"}), 404

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

    finally:
        if connection.is_connected():
            connection.close()


@volunteer_projects_endpoints.route('/readByUserID/<user_id>', methods=['GET'])
@jwt_required()
def readByUserID(user_id):
    """Routes for module get list volunteer_projects by user_id"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query untuk mengambil proyek donasi berdasarkan user_id
    select_query = """SELECT volunteer_project_id, title, description, target_amount, project_photo, current_amount, status, users.name, date_started
                      FROM volunteer_projects
                      INNER JOIN users ON volunteer_projects.user_id = users.user_id
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


# @volunteer_projects_endpoints.route('/read', methods=['GET'])
# @jwt_required()
# def read():
#     """Routes for module get list volunteer_projects with optional category filter"""
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     # Get 'category_id' from query parameters
#     category_id = request.args.get('category_id', None)

#     # Base query
#     select_query = "SELECT * FROM volunteer_projects"

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




@volunteer_projects_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create():
    """Routes for module create a blood_donation_projects"""
    required = get_form_data(["title"])  # use only if the field required
    title = required["title"]
    description = request.form['description']
    target_amount = request.form['target_amount']        
    user_id = request.form['user_id']
    date_started = request.form['date_started']

    uploaded_file = request.files.get('project_photo')
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        project_photo = uploaded_file.filename
    else:
        project_photo = 'default.jpg'  


    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO volunteer_projects (title, description, target_amount, project_photo, user_id, date_started) VALUES (%s, %s, %s, %s, %s, %s)"
    request_insert = (title, description, target_amount, project_photo, user_id, date_started)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    cursor.close()
    new_id = cursor.lastrowid  # Get the newly inserted book's ID\
    if new_id:
        return jsonify({"title": title, "message": "Inserted", "volunteer_projects_id": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@volunteer_projects_endpoints.route('/update/<volunteer_project_id>', methods=['PUT'])
@jwt_required()
def update(volunteer_project_id):
    """Routes for module update a donation project"""
    # Retrieve data from the request
    title = request.form.get('title')
    description = request.form.get('description')
    dateStarted = request.form.get('dateStarted')
    target_amount = request.form.get('target_amount')    
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

    if dateStarted:
        fields.append("date_started = %s")
        values.append(dateStarted)

    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        fields.append("project_photo = %s")
        values.append(uploaded_file.filename)

    # Ensure there are fields to update
    if fields:
        values.append(volunteer_project_id)
        connection = get_connection()
        cursor = connection.cursor()

        update_query = f"UPDATE volunteer_projects SET {', '.join(fields)} WHERE volunteer_project_id = %s"
        cursor.execute(update_query, values)

        if cursor.rowcount <= 0:
            return jsonify({"message": "Data not found"}), 400

        connection.commit()
        cursor.close()

        return jsonify({"message": "updated", "id_blood_donation_projects": volunteer_project_id}), 200

    return jsonify({"message": "No fields to update"}), 400



# @volunteer_projects_endpoints.route('/update/<donation_project_id>', methods=['PUT'])
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

#     update_query = "UPDATE volunteer_projects SET title=%s, description=%s, target_amount=%s, project_photo=%s, category_id=%s WHERE donation_project_id=%s"
#     update_request = (title, description, target_amount, project_photo, category_id, donation_project_id)
#     cursor.execute(update_query, update_request)
#     if cursor.rowcount <= 0:
#         return jsonify({"message": "Data not found"}), 400
#     connection.commit()
#     cursor.close()
#     data = {"message": "updated", "id_volunteer_projects": donation_project_id}
#     return jsonify(data), 200

# @volunteer_projects_endpoints.route('/volunteer', methods=['POST'])
# @jwt_required()
# def volunteer():
#     """Routes for module donate"""        
#     volunteer_project_id = request.form['volunteer_project_id']
#     user_id = request.form['user_id']
#     deskripsi = request.form['deskripsi']


#     connection = get_connection()
#     cursor = connection.cursor()
#     insert_query = "INSERT INTO volunteers (volunteer_project_id, user_id, deskripsi) VALUES (%s, %s, %s)"
#     request_insert = (volunteer_project_id, user_id, deskripsi)
#     cursor.execute(insert_query, request_insert)
#     connection.commit()  # Commit changes to the database
#     cursor.close()    
#     return jsonify({"volunteer_project_id": volunteer_project_id, "user_id": user_id, "deskripsi": deskripsi}), 201  

@volunteer_projects_endpoints.route('/volunteer', methods=['POST'])
@jwt_required()
def volunteer():
    """Routes for module donate"""
    volunteer_project_id = request.form['volunteer_project_id']
    user_id = request.form['user_id']
    deskripsi = request.form['deskripsi']
    umur = request.form['umur']

    connection = get_connection()
    cursor = connection.cursor()

    # Cek apakah user sudah terdaftar di project
    check_query = "SELECT COUNT(*) FROM volunteers WHERE volunteer_project_id = %s AND user_id = %s"
    cursor.execute(check_query, (volunteer_project_id, user_id))
    result = cursor.fetchone()

    if result[0] > 0:  # Jika sudah terdaftar
        cursor.close()
        return jsonify({"message": "Anda sudah terdaftar dalam proyek ini."}), 400

    # Jika belum terdaftar, tambahkan ke database
    insert_query = "INSERT INTO volunteers (volunteer_project_id, user_id, deskripsi, umur) VALUES (%s, %s, %s, %s)"
    request_insert = (volunteer_project_id, user_id, deskripsi, umur)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    cursor.close()

    return jsonify({"volunteer_project_id": volunteer_project_id, "user_id": user_id, "deskripsi": deskripsi}), 201


@volunteer_projects_endpoints.route('/delete/<volunteer_project_id>', methods=['DELETE'])
@jwt_required()
def delete(volunteer_project_id):
    """Routes for module to delete a donation project"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM volunteer_projects WHERE volunteer_project_id = %s"
    delete_id = (volunteer_project_id,)  # Perhatikan tanda koma di akhir untuk membuatnya menjadi tuple
    cursor.execute(delete_query, delete_id)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Data deleted", "volunteer_project_id": volunteer_project_id}
    return jsonify(data), 200

# @volunteer_projects_endpoints.route('/delete/<donation_project_id>', methods=['DELETE'])
# @jwt_required()
# def delete(donation_project_id):
#     """Routes for module to delete a book"""
#     connection = get_connection()
#     cursor = connection.cursor()

#     delete_query = "DELETE FROM volunteer_projects WHERE donation_project_id = %s"
#     delete_id = (donation_project_id)
#     cursor.execute(delete_query, delete_id)
#     if cursor.rowcount <= 0:
#         return jsonify({"message": "Data not found"}), 400
#     connection.commit()
#     cursor.close()
#     data = {"message": "Data deleted", "id_volunteer_projects": donation_project_id}
#     return jsonify(data)

@volunteer_projects_endpoints.route('/approve/<volunteer_project_id>', methods=['PUT'])
@jwt_required()
def approve(volunteer_project_id):
    """API to approve a donation project and update its status to 'approved'"""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status to 'approved'
    update_query = "UPDATE volunteer_projects SET status=%s WHERE volunteer_project_id=%s"
    update_request = ('approved', volunteer_project_id)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found or status already approved"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Status updated to approved", "id_volunteer_projects": volunteer_project_id}
    return jsonify(data), 200

@volunteer_projects_endpoints.route('/reject/<volunteer_project_id>', methods=['PUT'])
@jwt_required()
def reject(volunteer_project_id):
    """API to reject a donation project and update its status to 'rejected'"""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status to 'rejected'
    update_query = "UPDATE volunteer_projects SET status=%s WHERE volunteer_project_id=%s"
    update_request = ('rejected', volunteer_project_id)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found or status already rejected"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Status updated to rejected", "id_volunteer_projects": volunteer_project_id}
    return jsonify(data), 200




@volunteer_projects_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't upload data"}), 400


@volunteer_projects_endpoints.route('/donate', methods=['POST'])
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

@volunteer_projects_endpoints.route('/approveVolunteer/<volunteer_id>', methods=['PUT'])
@jwt_required()
def approveDonor(volunteer_id):
    """API to approve a donation project and update its status to 'approved'"""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status to 'approved'
    update_query = "UPDATE volunteers SET status=%s WHERE volunteer_id=%s"
    update_request = ('approved', volunteer_id)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found or status already approved"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Status updated to approved", "volunteer_id": volunteer_id}
    return jsonify(data), 200 

@volunteer_projects_endpoints.route('/rejectVolunteer/<volunteer_id>', methods=['PUT'])
@jwt_required()
def rejectDonor(volunteer_id):
    """API to reject a donation project and update its status to 'rejected'"""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status to 'rejected'
    update_query = "UPDATE volunteers SET status=%s WHERE volunteer_id=%s"
    update_request = ('rejected', volunteer_id)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        return jsonify({"message": "Data not found or status already rejected"}), 400

    connection.commit()
    cursor.close()
    data = {"message": "Status updated to rejected", "volunteer_id": volunteer_id}
    return jsonify(data), 200

@volunteer_projects_endpoints.route('/readVolunteredByID/<int:volunteer_project_id>', methods=['GET'])
@jwt_required()
def readVolunteered_by_id(volunteer_project_id):
    """Route to get a single donation project by its ID"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        select_query = """
        SELECT 
    volunteers.volunteer_id, 
    volunteer_projects.title AS project_title, 
    users.name AS volunteer_name, 
    volunteers.deskripsi, 
    volunteers.status, 
    volunteers.volunteer_project_id,
    volunteers.umur
FROM 
    volunteers
INNER JOIN 
    volunteer_projects ON volunteers.volunteer_project_id = volunteer_projects.volunteer_project_id
INNER JOIN 
    users ON volunteers.user_id = users.user_id
WHERE volunteers.user_id = %s;
        """

        cursor.execute(select_query, (volunteer_project_id,))
        result = cursor.fetchall()  # Fetch only one record

        cursor.close()

        if result:
            return jsonify({"message": "OK", "data": result}), 200
        else:
            return jsonify({"message": "Donation project not found"}), 404

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

    finally:
        if connection.is_connected():
            connection.close()