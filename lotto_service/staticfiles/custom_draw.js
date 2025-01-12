document.addEventListener("DOMContentLoaded", function() {
    const randomButton = document.createElement("button");
    randomButton.type = "button";
    randomButton.textContent = "Generate Random Numbers";
    randomButton.style.marginBottom = "10px";

    const form = document.querySelector("form");
    const winningNumbersField = document.getElementById("id_winning_numbers");
    const bonusNumberField = document.getElementById("id_bonus_number");

    randomButton.addEventListener("click", function() {
        const winningNumbers = Array.from({ length: 6 }, () => Math.floor(Math.random() * 45) + 1);
        const bonusNumber = Math.floor(Math.random() * 45) + 1;

        winningNumbersField.value = winningNumbers.join(",");
        bonusNumberField.value = bonusNumber;
    });

    if (form) {
        form.insertBefore(randomButton, form.firstChild);
    }
});
