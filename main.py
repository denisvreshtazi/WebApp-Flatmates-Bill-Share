from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill.bill import Bill
from flatmates_bill.flatmate import Flatmate

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):
    def get(self):
        bill_form = BillForm()

        return render_template('bill_form_page.html',
                               billform=bill_form)
    def post(self):
        bill_form = BillForm(request.form)
        amount = bill_form.amount.data
        period = bill_form.period.data
        the_bill = Bill(float(amount), period)

        name1 = bill_form.name1.data
        days_in_house1 = bill_form.days_in_house1.data

        name2 = bill_form.name2.data
        days_in_house2 = bill_form.days_in_house2.data

        flatmate1 = Flatmate(name1, float(days_in_house1))
        flatmate2 = Flatmate(name2, float(days_in_house2))

       # return f"{flatmate1.name} pays: {flatmate1.pays(the_bill, flatmate2)}"

        return render_template('bill_form_page.html',
                                result=True,
                                billform=bill_form,
                                name1=flatmate1.name,
                                amount1=flatmate1.pays(the_bill, flatmate2),
                                name2=flatmate2.name,
                                amount2=flatmate2.pays(the_bill, flatmate1)
                           )

class ResultsPage(MethodView):

    def post(self):
        bill_form = BillForm(request.form)
        amount = bill_form.amount.data
        period = bill_form.period.data
        the_bill = Bill(float(amount), period)

        name1 = bill_form.name1.data
        days_in_house1 = bill_form.days_in_house1.data

        name2 = bill_form.name2.data
        days_in_house2 = bill_form.days_in_house2.data

        flatmate1 = Flatmate(name1, float(days_in_house1))
        flatmate2 = Flatmate(name2, float(days_in_house2))

       # return f"{flatmate1.name} pays: {flatmate1.pays(the_bill, flatmate2)}"

        return render_template('bill_form_page.html',
                                name1=flatmate1.name,
                                amount1=flatmate1.pays(the_bill, flatmate2),
                                name2=flatmate2.name,
                                amount2=flatmate2.pays(the_bill, flatmate1)
                           )


class BillForm(Form):
    amount = StringField("Bill Amount: ", default="100")
    period = StringField("Period", default="January 2023")

    name1 = StringField("Name: ", default="Mary")
    days_in_house1 = StringField("Days in the house: ", default="25")

    name2 = StringField("Name: ", default="Luca")
    days_in_house2 = StringField("Days in the house: ", default="20")

    button = SubmitField("Calculate")


app.add_url_rule('/',
                 view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form',
                 view_func=BillFormPage.as_view('bill_form_page'))
# app.add_url_rule('/results',
#                  view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)
