"""Budget resources"""
from flask_restful import Resource, reqparse, fields, marshal
from datetime import datetime
from api.models.budget_models import Budget
from api import db
from flask_login import current_user, login_required

    
budget_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'amount': fields.Float(attribute=lambda x: round(x.amount, 2)),
    'start_date': fields.String(attribute=lambda x: x.start_date.strftime('%Y-%m-%d')),
    'end_date': fields.String(attribute=lambda x: x.end_date.strftime('%Y-%m-%d')),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class AllUserBudgets(Resource):
    """/users/id/budgets route handler"""
    @login_required
    def post(self, id):
        """POST /users/id/budgets """
        try:
            if current_user.id == id or current_user.rank == 1:
                parser = reqparse.RequestParser()
                parser.add_argument('name', help='This field is required', type = str, location = 'json', required=True)
                parser.add_argument('amount', help='This field is required', type = float, location = 'json', required=True)
                parser.add_argument('start_date', help='This field is required', type = str, location = 'json', required=True)
                parser.add_argument('end_date', help='This field is required', type = str, location = 'json', required=True)
                data = parser.parse_args()
                
                start_date_str = data['start_date']
                end_date_str = data['end_date']
                start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
                end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()

                new_budget = Budget(
                    user_id=current_user.id,
                    name=data['name'],
                    amount=data['amount'],
                    start_date=start_date,
                    end_date=end_date
                )

                db.session.add(new_budget)
                db.session.commit()
                return {'message': 'Budget added successfully', 'data': data }, 201
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception:
            return {'message': 'An error occured, ensure you are using the right keys, datatypes and your request body is properly formatted'}, 400


    @login_required
    def get(self, id):
        """GET /users/id/budgets """
        try:
            if current_user.id == id or current_user.rank == 1:
                budgets = Budget.query.filter_by(user_id=id).all()
                print(budgets)
                if budgets:
                    # Use marshal to serialize the budget object
                    serialized_budgets = marshal(budgets, budget_fields)
                    print(serialized_budgets)
                    return {'message': 'Successful', 'data': serialized_budgets}
                else:
                    return {'message': 'Budgets not found'}, 404
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        

    
class Budgets(Resource):
    """/users/<int:id>/budgets/<int:budget_id> route handler"""
    @login_required
    def get(self, id, budget_id):
        """GET /users/<int:id>/budgets/<int:budget_id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter_by(user_id=id, id=budget_id).first()
                if budget:
                    # Use marshal to serialize the budget object
                    budget = marshal(budget, budget_fields)
                    return {'message': 'Successful', 'data': budget}
                else:
                    return {'message': 'Budget not found'}, 404
            else:
                return {'message': "You are trying to access another user's budget"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        
    @login_required
    def put(self, id, budget_id):
        """ PUT /users/<int:id>/budgets/<int:budget_id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                parser = reqparse.RequestParser()
                parser.add_argument('name', help='This field is required', type = str, location = 'json')
                parser.add_argument('amount', help='This field is required', type = float, location = 'json')
                parser.add_argument('start_date', help='This field is required', type = str, location = 'json')
                parser.add_argument('end_date', help='This field is required', type = str, location = 'json')
                data = parser.parse_args()
                print(id)
                budget = Budget.query.filter((Budget.user_id == id) & (Budget.id == budget_id)).first()
                print(id)

                if not budget:
                    return {'message': 'Budget not found'}, 404

                # Update budget attributes if the fields are provided in the request
                if data['name']:
                    budget.name = data['name']
                if data['amount']:
                    budget.amount = data['amount']
                if data['start_date']:
                    start_date_str = data['start_date']
                    start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
                    budget.start_date = start_date
                if data['end_date']:
                    end_date_str = data['end_date']
                    end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
                    budget.end_date = end_date

                db.session.commit()

                return {'message': 'Budget updated successfully', 'data': {k: v for k, v in data.items() if v is not None}}

            else:
                return {'message': "You are not authorized to update this budget"}, 403
        except Exception as err:
            print(err)
            return {'message': 'An error occured, ensure you are using the right keys, datatypes and your request body is properly formatted'}, 400
        
    @login_required
    def delete(self, id, budget_id):
        """DELETE /users/<int:id>/budgets/<int:budget_id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter((Budget.user_id == id) & (Budget.id == budget_id)).first()

                if budget:
                    db.session.delete(budget)
                    db.session.commit()
                    return {'message': 'Budget Deleted Successfully', 'data': {'id': budget.id, 'name': budget.name}}
                else:
                    return {'message': 'Budget not found'}, 404
            else:
                return {'message': "You are trying to access another user's budget"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again, ensure your request is correct!'}, 500
