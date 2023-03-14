error_list = (typeof (error_list) == 'undefined') ? document.getElementById('error-list') : error_list;
if (error_list) {
    let fields = error_list.children;
    for (let field of fields) {
        if (field.dataset.all) {
            // for __all__
            let all_inputs = document.querySelectorAll('input, select, textarea');
            for (input of all_inputs) {
                if (!['hidden', 'button', 'image', 'submit', 'reset', 'search'].includes(input.type)) {
                    input.classList.add('is-invalid');
                }
            }
            break;
        }
        else {
            let field_name = field.dataset.fieldName;
            let invalid_inputs = document.querySelectorAll(`input[name=${field_name}], select[name=${field_name}], textarea[name=${field_name}]`);
            for (let invalid_input of invalid_inputs) {
                invalid_input.classList.add('is-invalid');
            }
        }
    }
}
