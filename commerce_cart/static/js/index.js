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
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".add__to__cart__btn");

  buttons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const productId = btn.dataset.productId;
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      try {
        const response = await fetch("/add-to-cart/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken,
          },
          body: new URLSearchParams({ product_id: productId }),
        });

        const data = await response.json();

        if (data.success) {
          btn.textContent = "Item Added.";
          btn.disabled = true;

          showToast(data.message || "Added to cart");
        } else {
          showToast(data.error || "Failed to add", true);
        }
      } catch (err) {
        showToast("Network error", true);
      }
    });
  });

  function showToast(msg, isError = false) {
    const toast = document.createElement("div");
    toast.textContent = msg;
    toast.className = `toast ${isError ? "error" : "success"}`;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 3000);
  }
});
