from db.db_connection import query_dynamic_user_inputs

# Query all rows in the UserInputs table
print("All entries in the database:")
results = query_dynamic_user_inputs()  # No parameters to get all rows
for row in results:
    print(f"ID: {row[0]}, Website: {row[1]}, Field Name: {row[2]}, Field Value: {row[3]}, Timestamp: {row[4]}")
