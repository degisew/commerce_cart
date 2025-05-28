// Automatically close alerts after 4 seconds
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".auto-dismiss-alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
      alertInstance.close();
    }, 5000);
  });
});

// Updating quantity and line price
document.addEventListener("DOMContentLoaded", function () {
  const qtyInputs = document.querySelectorAll(".quantity-input");

  function updateCartTotals() {
    let total = 0;

    qtyInputs.forEach((input) => {
      const productId = input.dataset.productId;
      const price = parseFloat(input.dataset.price);
      const quantity = parseInt(input.value) || 0;
      const lineTotal = (price * quantity).toFixed(2);

      document.getElementById(
        `line-total-${productId}`
      ).innerText = `AED ${lineTotal}`;
      total += parseFloat(lineTotal);
    });

    document.getElementById("grand-total").innerText = `AED ${total.toFixed(
      2
    )}`;
  }

  qtyInputs.forEach((input) => {
    input.addEventListener("input", updateCartTotals);
  });
});

// Add to cart
document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll(".add-to-cart-form");

  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const productId = this.dataset.productId;
      const url = this.dataset.url;
      const button = this.querySelector(".add__to__cart__btn");
      const btnText = button.querySelector(".btn-text");
      const spinner = button.querySelector(".spinner-border");

      const csrfToken = this.querySelector("[name=csrfmiddlewaretoken]").value;

      const formData = new FormData();
      formData.append("product_id", productId);
      formData.append("csrfmiddlewaretoken", csrfToken);

      // AJAX request
      fetch("/commerce/add-to-cart/", {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            showToast("Success!", data.message, "success");
          } else {
            showToast("Error!", data.message, "error");
          }
        })
        .catch((error) => {
          console.error("Error:", error);

          showToast(
            "Error!",
            "Something went wrong. Please try again.",
            "error"
          );
        });
    });
  });
});

// Toast notification
function showToast(title, message, type = "success") {
  const toastContainer = document.getElementById("toast-container");
  const toastId = "toast-" + Date.now();

  const bgClass = type === "success" ? "bg-success" : "bg-danger";

  const toastHTML = `
        <div class="toast align-items-center text-white ${bgClass} border-0" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="3000">
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${title}</strong><br>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

  toastContainer.insertAdjacentHTML("beforeend", toastHTML);

  const toastElement = document.getElementById(toastId);
  const toast = new bootstrap.Toast(toastElement);
  toast.show();

  toastElement.addEventListener("hidden.bs.toast", function () {
    this.remove();
  });
}
