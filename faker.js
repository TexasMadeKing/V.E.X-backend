from faker import Faker

faker = Faker()

@app.route('/populate_users', methods=['GET'])
def populate_users():
    num_users = 10  # Number of fake users to add
    for _ in range(num_users):
        fake_email = faker.email()
        fake_password = faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        new_user = User(fake_email, fake_password)
        db.session.add(new_user)
    db.session.commit()
    return {'message': f'Successfully added {num_users} fake users'}

    if __name__ == '__main__':
    host = 'localhost'
    port = 5000

    print("\nPostman Client Endpoints:\n" + "="*30)
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        print(f"Method(s): {methods} -> Endpoint: http://{host}:{port}{rule}")
    
    with app.app_context():
        db.create_all()
        # populate_users()
        app.run(debug=True, host=host, port=port)