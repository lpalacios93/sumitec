window.CatalogPicker = {
    open(url) {
        window.open(
            url,
            "catalogPicker",
            "width=760,height=680,resizable=yes,scrollbars=yes"
        );
    },
    select(fieldId, value, label) {
        const select = document.getElementById(fieldId);
        if (!select) {
            return;
        }
        let option = Array.from(select.options).find((item) => item.value === String(value));
        if (!option) {
            option = new Option(label, value, true, true);
            select.add(option);
        }
        select.value = value;
    },
};

document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-picker-url]");
    if (!button) {
        return;
    }
    event.preventDefault();
    window.CatalogPicker.open(button.dataset.pickerUrl);
});
