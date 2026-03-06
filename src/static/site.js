let lastFocusedElement = null;
const getModalEl = () => document.querySelector('#modal-mount-point > .modal');
document.addEventListener('hidden.bs.modal', function (event) {
    const modalInstance = bootstrap.Modal.getInstance(getModalEl());
    if (modalInstance) {
        modalInstance.dispose();
    }
    document.querySelector('#modal-mount-point').innerHTML = '';
    if (lastFocusedElement) {
        lastFocusedElement.focus();
    }
});
function openModal() {
    lastFocusedElement = document.activeElement;
    const modalInstance = bootstrap.Modal.getOrCreateInstance(getModalEl());
    modalInstance.show()
}
document.addEventListener('activate-modal', function (event) {
    openModal();
});
