function createNewLogModal(courseSectionId) {
    
  // Create the modal container
  const modalContainer = document.createElement('div');
  modalContainer.className = 'modal fade';
  modalContainer.id = 'staticBackdrop';
  modalContainer.setAttribute('data-bs-backdrop', 'static');
  modalContainer.setAttribute('data-bs-keyboard', 'false');
  modalContainer.setAttribute('tabindex', '-1');
  modalContainer.setAttribute('aria-labelledby', 'staticBackdropLabel');
  modalContainer.setAttribute('aria-hidden', 'true');
  

  // Create the modal dialog
  const modalDialog = document.createElement('div');
  modalDialog.className = 'modal-dialog modal-dialog-centered';

  // Create the modal content
  const modalContent = document.createElement('div');
  modalContent.className = 'modal-content';

  // Create the modal header
  const modalHeader = document.createElement('div');
  modalHeader.className = 'modal-header';

  const modalTitle = document.createElement('h1');
  modalTitle.className = 'modal-title fs-5';
  modalTitle.id = 'staticBackdropLabel';
  modalTitle.textContent = 'Create a new Log';

  const closeButton = document.createElement('button');
  closeButton.type = 'button';
  closeButton.className = 'btn-close';
  closeButton.setAttribute('data-bs-dismiss', 'modal');
  closeButton.setAttribute('aria-label', 'Close');

  modalHeader.appendChild(modalTitle);
  modalHeader.appendChild(closeButton);

  // Create the modal body
  const modalBody = document.createElement('div');
  modalBody.className = 'modal-body';

  const container = document.createElement('div');
  container.className = 'container';

  // Create the form
  const form = document.createElement('form');

  // Lecture ID (hidden field)
  const courseSectionIdInput = document.createElement('input');
  courseSectionIdInput.type = 'hidden';
  courseSectionIdInput.name = 'lecture_id';
  courseSectionIdInput.value = courseSectionId;

  // Type Dropdown
  const typeDropdown = document.createElement('div');
  typeDropdown.className = 'mb-3';

  const typeLabel = document.createElement('label');
  typeLabel.htmlFor = 'logType';
  typeLabel.className = 'form-label';
  typeLabel.textContent = 'Type';

  const typeSelect = document.createElement('select');
  typeSelect.className = 'form-select';
  typeSelect.id = 'logType';
  typeSelect.name = 'logType';
  typeSelect.required = true;

  const defaultOption = document.createElement('option');
  defaultOption.value = '';
  defaultOption.selected = true;
  defaultOption.disabled = true;
  defaultOption.textContent = 'Select Type';

  const logTypes = [
      ['VS', 'View Session'],
      ['EX', 'Exercise'],
      ['WS', 'Work Session'],
      ['RV', 'Review'],
      ['RD', 'Reading'],
      ['OT', 'Other'],
      ['FI', 'Finish']
  ];

  logTypes.forEach(([value, label]) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = label;
      typeSelect.appendChild(option);
  });

  typeDropdown.appendChild(typeLabel);
  typeDropdown.appendChild(typeSelect);

  // Content Text Field
  const contentTextField = document.createElement('div');
  contentTextField.className = 'mb-3';

  const contentLabel = document.createElement('label');
  contentLabel.htmlFor = 'logContent';
  contentLabel.className = 'form-label';
  contentLabel.textContent = 'Content';

  const contentTextarea = document.createElement('textarea');
  contentTextarea.className = 'form-control';
  contentTextarea.id = 'logContent';
  contentTextarea.name = 'logContent';
  contentTextarea.rows = '3';
  contentTextarea.required = true;

  contentTextField.appendChild(contentLabel);
  contentTextField.appendChild(contentTextarea);

  // Time Spent Field
  const timeSpentField = document.createElement('div');
  timeSpentField.className = 'mb-3';

  const timeSpentLabel = document.createElement('label');
  timeSpentLabel.htmlFor = 'timeSpent';
  timeSpentLabel.className = 'form-label';
  timeSpentLabel.textContent = 'Time Spent (minutes)';

  const timeSpentInput = document.createElement('input');
  timeSpentInput.type = 'number';
  timeSpentInput.className = 'form-control';
  timeSpentInput.id = 'timeSpent';
  timeSpentInput.name = 'timeSpent';
  timeSpentInput.required = true;

  timeSpentField.appendChild(timeSpentLabel);
  timeSpentField.appendChild(timeSpentInput);

  // Submit Button
  const submitButton = document.createElement('button');
  submitButton.type = 'submit';
  submitButton.className = 'btn btn-primary';
  submitButton.textContent = 'Submit';

  form.appendChild(courseSectionIdInput);
  form.appendChild(typeDropdown);
  form.appendChild(contentTextField);
  form.appendChild(timeSpentField);
  form.appendChild(submitButton);

  container.appendChild(form);
  modalBody.appendChild(container);

// EVENT LISTENER
  // Add a submit event listener to the form
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Get form data
    let logType = typeSelect.value;
    let logContent = contentTextarea.value;
    let timeSpent = timeSpentInput.value;

    // Call the createLog function with form data and courseSectionId
    createLog(logType, logContent, timeSpent, courseSectionId)
    .then(response =>{
      bootstrapModal.hide();
    })

    

  });
  
  // Create the modal footer
  const modalFooter = document.createElement('div');
  modalFooter.className = 'modal-footer';

  const closeButtonFooter = document.createElement('button');
  closeButtonFooter.type = 'button';
  closeButtonFooter.className = 'btn btn-secondary';
  closeButtonFooter.setAttribute('data-bs-dismiss', 'modal');
  closeButtonFooter.textContent = 'Close';

  modalFooter.appendChild(closeButtonFooter);

  // Append all elements to the modal content
  modalContent.appendChild(modalHeader);
  modalContent.appendChild(modalBody);
  modalContent.appendChild(modalFooter);

  // Append modal content to modal dialog
  modalDialog.appendChild(modalContent);

  // Append modal dialog to modal container
  modalContainer.appendChild(modalDialog);

  const bootstrapModal = new bootstrap.Modal(modalContainer);
  bootstrapModal.show();

}



// ========================================
// SECTION 1: Event handlers inside modals
//=========================================
