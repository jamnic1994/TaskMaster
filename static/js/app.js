function toggleEdit(groupId) {
    var groupName = document.getElementById("group-name-" + groupId);
    var groupDescription = document.getElementById("group-description-" + groupId);
    var editBtn = document.getElementById("edit-btn-" + groupId);
    var confirmBtn = document.getElementById("confirm-btn-" + groupId);

    // Toggle the readonly/disabled state of the inputs and textarea
    if (groupName.readOnly !== undefined) {
        groupName.readOnly = !groupName.readOnly;
    }
    if (groupDescription.readOnly !== undefined) {
        groupDescription.readOnly = !groupDescription.readOnly;
    }

    // Toggle the visibility of buttons
    editBtn.style.display = groupName.readOnly ? "inline-block" : "none";
    confirmBtn.style.display = groupName.readOnly ? "none" : "inline-block";
}