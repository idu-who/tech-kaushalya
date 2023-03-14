// toggle between expand and collapse icons
member_forms = $('.collapse.member-form');

function toggle_icon_handler(event) {
    let member_form = event.target;
    let member_no = member_form.dataset.memberNo;
    let toggle_icon = document.querySelector(`#member-header-${member_no}>.toggle-icon`);
    if (toggle_icon) {
        if (toggle_icon.classList.contains('bi-plus-lg')) {
            toggle_icon.classList.replace('bi-plus-lg', 'bi-dash-lg')
        }
        else {
            toggle_icon.classList.replace('bi-dash-lg', 'bi-plus-lg')
        }
    }
}
member_forms.on('shown.bs.collapse', toggle_icon_handler);
member_forms.on('hidden.bs.collapse', toggle_icon_handler);

// handle disabled member
function prepare_next_disabled_header(current_disabled_header = undefined) {
    if (typeof current_disabled_header === 'undefined') {
        current_disabled_header = document.querySelector('.card-header.disabled');
    }
    if (current_disabled_header) {
        current_disabled_header.onclick = disabled_click_handler;
    }
}
prepare_next_disabled_header();

function disabled_click_handler(event) {
    let target = event.target;
    let header = target;

    if (target.tagName == 'I') {
        header = target.parentElement;
    }

    if (empty_fields()) {
        window.alert('Please complete current members details before adding additional members.');
        return;
    }
    enable_member(header);
}

function empty_fields() {
    let registration_form_inputs = document.querySelectorAll('#registration-form input:not(:disabled)');
    for (let input of registration_form_inputs) {
        if (input.validity.valueMissing) {
            return true
        }
    }
    return false;
}

function enable_member(header) {
    let toggle_button = header.parentElement;
    toggle_button.dataset.toggle = 'collapse';
    header.classList.remove('disabled');
    header.onclick = null;
    prepare_next_disabled_header();
    enable_inputs(toggle_button.dataset.target.substr(1));
}

function enable_inputs(member_form_id) {
    let member_form_inputs = document.querySelectorAll(`#${member_form_id} input`);
    for (let member_form_input of member_form_inputs) {
        member_form_input.removeAttribute('disabled');
        member_form_input.setAttribute('required', '');
    }
}

// handle enabled member cancel
cancel_member_buttons = document.querySelectorAll('.cancel-member');
cancel_member_buttons.forEach((cancel_member_button) => {
    cancel_member_button.onclick = disable_member;
});

function disable_member(event) {
    let cancel_member_button = event.target;
    let toggle_button = cancel_member_button.parentElement.previousElementSibling;
    let header = toggle_button.firstElementChild;
    toggle_button.dataset.toggle = '';
    header.classList.add('disabled');
    prepare_next_disabled_header(header);
    disable_inputs(toggle_button.dataset.target.substr(1));
}

function disable_inputs(member_form_id) {
    let member_form_inputs = document.querySelectorAll(`#${member_form_id} input`);
    for (let member_form_input of member_form_inputs) {
        member_form_input.setAttribute('disabled', '');
        member_form_input.removeAttribute('required');
    }
}
