# from django.shortcuts import redirect, render
# from django.urls import reverse_lazy
# from django.views import View

# from book_store.users.forms import CustomUserCreationForm


# class SignupPageView(View):  # can be done by generic CreateView
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {"form": form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(self.success_url)
#         return render(request, self.template_name, {"form": form})
