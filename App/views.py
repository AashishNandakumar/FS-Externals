from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.template import Template, Context, loader
from .models import *
from .forms import *
import csv

# Create your views here.

"""
Object-Based Generic Views
    -> object based generic views are class based generic views that provided common functionalities to display and manipulate DB objects
    -> these generic based views abstract away much of the boilerplate code needed for common functionalities

    Advantages:
        1. Code reusability
        2. Rapid development
        3. Consistency
        4. Flexibility (we can extend the functionalities provided by generics)
        5. built-in features
"""


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"


"""
Function-based Generic Views
    -> similar to class-based generic views but has less flexibility (but is simple)
"""


def book_list(request):
    return ListView.as_view(
        model=Book,
        template_name="book_list.html",
        context_object_name="books",
    )(request)


"""
Extending Generic-Views in Django
    -> allows for customization and enhancing the functionalities
    -> includes sub-classing generic views and overriding or extending the methods or attributes
    why is it beneficial?
        1. Customization
        2. Flexibility
        3. Reusability
        4. Code Organization
        5. Maintainability
"""


# 1. Overriding methods
class CustomBookListView(ListView):
    model = Book

    def get_queryset(self):
        # make this function to return only published books
        return Book.objects.filter(published=True)


# 2. Using Mixins
class PrivateBookListView(LoginRequiredMixin, ListView):
    # allow only logged in users to use this View
    model = Book


# 3. customizing attributes
class TopBookListView(ListView):
    model = Book
    # the queryset by default will be ordered according to "rating" and will only contain 10 elements
    queryset = Book.objects.order_by("rating")[:10]


# 4. adding extra context
class BookListWithPublishersView(ListView):
    model = Book

    def get_context_data(self, **kwargs):
        # add extra content to the existing content
        context = super().get_context_data(**kwargs)
        # add a new key-value pair to the context
        context["publishers"] = Publisher.objects.all()
        return context


"""
MIME in Django Views
    -> Multi-Purpose Internet Mail Extensions are handled in django-views by setting the 'Content-Type' header in HTTP response
"""


def generate_tie_students_csv(request):
    response = HttpResponse(content_type="text/csv")
    # this instructs the browser to download the file instead of displaying it
    response["Content-Disposition"] = 'attachment;filename="tie_students.csv"'

    writer = csv.writer(response)
    writer.writerow(["Username", "City", "College", "Branch"])

    students = Student.objects.all()

    for student in students:
        writer.writerow(
            [student.username, student.city, student.college, student.branch]
        )

    return response


def generate_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment;filename="sample.pdf"'

    # create a PDF object
    p = canvas.Canvas(response)

    # draw on the object
    p.drawString(100, 100, "Hello, World!")

    # close the PDF object
    p.showPage()
    p.save()

    return response


"""
High-Level Syndication Feed Generating Framework in Django
    -> Feed is a way to share latest information in ur website with other so that they dont have to browse the entire website
    -> think of it as a form which which contains links to the latest informations of the website, saving u time without having
        to browse the website to search for new updates
"""


class LatestBookFeed(Feed):
    title = "Latest Books"
    description = "Latest books added to our catalog"
    link = "/books/"

    def items(self):
        return Book.objects.order_by("-pub_date")[:5]

    def item_title(self, item):
        return item.title

    def item_abstract(self, item):
        return item.abstract

    def item_link(self, item):
        return reverse("book_detail", args=[item.pk])


class AtomBooksFeed(LatestBookFeed):
    feed_type = Atom1Feed
    subtitle = LatestBookFeed.description


def book_detail(request, pk):
    return HttpResponse(f"you have requested book number: {pk}, pls wait!")


"""
Cookies
    -> Are small pieces of data stored on the browser by the website
    -> They are useful for maintaining stateful information for the stateless HTTP protocol
    -> how are they beneficial?
        1. Session management - keeps users logged in across multiple pages
        2. Personalization - remembering user preferences
        3. Tracking - monitoring the user's activities on the website
"""


def set_cookie(request):
    response = HttpResponse("Cookie Set!")
    response.set_cookie("favourite_color", "blue", max_age=3600)

    return response


def get_cookie(request):
    favourite_color = request.COOKIES.get("favourite_color", "Not set")
    return render(request, "cookie_template.html", {"color": favourite_color})


"""
    A search application using AJAX that displays internship domain enrolled by a student searched
"""


def search_view(request):
    return render(request, "search.html")


def search_internship(request):
    query = request.GET.get("query", "")
    try:
        student = StudentNew.objects.get(name__icontains=query)
        domains = student.internship_domains.all().values_list("name", flat=True)
        return JsonResponse({"domains": list(domains)})
    except StudentNew.DoesNotExist:
        return JsonResponse({"domains": []})


"""
    A registration page for student enrollment using AJAX
"""


def registration_view(request):
    form = StudentNewRegistrationForm()
    return render(request, "register.html", {"form": form})


def register_student(request):
    if request.method == "POST":
        form = StudentNewRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"success": True, "message": "Student registered successfully"}
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})


# FeedbackForm processing
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # process cleaned data
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            feedback = form.cleaned_data.get("feedback")

            # save to database
            Feedback.objects.create(name=name, email=email, feedback=feedback)
            return redirect("feedback_success")
    else:
        form = FeedbackForm()

    return render(request, "feedback_form.html", {"form": form})


def feedback_success(request):
    return HttpResponse("Feedback successfully submitted")


"""
Template and Context
    -> Templates defines the structure of the page acting as a template with placeholders
    -> Context contains the data that is to be injected into the template's placeholders
"""


def render_simple_template(request):
    template_string = "Hello, {{name}}"
    template = Template(template_string)
    context = Context({"name": "Aashish Nandakumar"})
    rendered_string = template.render(context)
    return HttpResponse(rendered_string)


"""
Filters - modifies  the values of the variables
    Examples of filters:
        1. {{name|lower}} - lowercasing
        2. {{blog|truncatewords:30}} - limit(display) the name to only 30 words
        3. {{students|join:", "}} - join the list of students and sperate them via `,`
        4. {{age|default:18}} - set age = 18 if the value of age is absent
        5. {{DOB|date:"Y-m-d"}} - date formatting
"""

"""
Context Variable Lookup
    -> use dot notation to access attributes of variables
    -> example:
        1. {{person.name}}
        2. {{dict.key}}
        3. {{list.0}}
"""


"""
Load templates
"""


def load_template(request):
    template = loader.get_template("cookie_template.html")
    return HttpResponse(template.render())


"""
Template Tags
    -> Are special components in templates used along with context variables
    -> examples:
        1. {% if condition %}{% endif %}
        2. {% for item in items}{% endfor %}
        3. {% block name %}{% endblock %}
        4. {% include 'footer.html' %}
        5. {% extends 'base.html' %}
        6. {% url 'name' %}
"""

"""
Web Frameworks
    -> Is a tool that makes it easy to develop web applications by providing a structured and a defined approach
    -> They provide components, libraries and best practices which helps the developers build maintainable, scalable
        web applications

    Advantages:
        1. Rapid development
        2. Consistency
        3. Security
        4. Scalability
        5. Community Support

    Disdvantages:
        1. Learning Curve
        2. Flexibility Limitations
        3. Performance overhead
        4. Compatibilty issues
        5. Higher Resource Consumption
"""

"""
MVC design pattern
    1. Model - handles data and business logic
    2. View - presentation layer
    3. Controller - intermediary (Communication Broker) between Models and Views

    Advantages:
        1. Seperation of concerns (modular)
        2. Reusability
        3. Parallel development
        4. Easier Testing
        5. Flexibilty (loose-coupling)
"""


"""
Custom Error Pages
"""


def custom_404_view(request, exception):
    return HttpResponse("woops page not found", status=404)


def get_two_nos(request, no1, no2):
    return HttpResponse(f"received {no1} and {no2}")


def validate_phonenumber(request, phone_number: str):
    if phone_number.startswith("+"):
        phone_number = phone_number[1:]

    if len(phone_number) == 10 and phone_number[0] != "0" and phone_number.isdigit():
        return HttpResponse("Valid phone number")
    return HttpResponse("Invalid phone number")
