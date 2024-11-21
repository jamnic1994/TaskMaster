// JavaScript to toggle the ability to edit group details from the manage_groups page
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

// JavaScript to toggle between Task View and Group View on index page
const viewToggle = document.getElementById('viewToggle');
const taskView = document.getElementById('taskView');
const groupView = document.getElementById('groupView');

viewToggle.addEventListener('change', function() {
    if (viewToggle.checked) {
        taskView.style.display = 'none';
        groupView.style.display = 'block';
    } else {
        taskView.style.display = 'block';
        groupView.style.display = 'none';
    }
});

function confirmCompletion(taskId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "This task will be marked as completed!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, mark it complete!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById(`completeTaskForm-${taskId}`).submit();
        }
    });
}