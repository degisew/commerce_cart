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
        ).innerText = `$${lineTotal}`;
        total += parseFloat(lineTotal);
      });

      document.getElementById("grand-total").innerText = `$${total.toFixed(2)}`;
    }

    qtyInputs.forEach((input) => {
      input.addEventListener("input", updateCartTotals);
    });
  });
