function inviteMember() {
  const inviteMemberForm = document.querySelector("#invite-member-form");
  const emailField = inviteMemberForm.querySelector("#invite-member-email");
  const saveInviteMember = inviteMemberForm.querySelector(
    "#invite-member-button"
  );
  const roleFields = Array.prototype.slice.call(
    inviteMemberForm.querySelectorAll(".p-checkbox__input")
  );

  emailField.addEventListener("change", function () {
    const checkedFields = roleFields.filter(function (field) {
      return field.checked;
    });

    if (emailField.value && checkedFields.length) {
      saveInviteMember.disabled = false;
    } else {
      saveInviteMember.disabled = true;
    }
  });

  roleFields.forEach(function (field) {
    field.addEventListener("change", function () {
      const checkedFields = roleFields.filter(function (field) {
        return field.checked;
      });

      if (emailField.value && checkedFields.length) {
        saveInviteMember.disabled = false;
      } else {
        saveInviteMember.disabled = true;
      }
    });
  });

  inviteMemberForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const form = e.target;
    const inviteMembersField = form.querySelector("#invite-members");
    const emailField = form.querySelector("#invite-member-email");
    const roleFields = Array.prototype.slice.call(
      form.querySelectorAll(".p-checkbox__input")
    );

    const members = [];
    const newMember = {
      email: emailField.value,
      roles: [],
    };

    roleFields.forEach(function (role) {
      if (role.checked) {
        newMember.roles.push(role.name);
      }
    });

    members.push(newMember);

    inviteMembersField.value = JSON.stringify(members);

    form.submit();
  });
}

function updateMembers(membersData) {
  membersData = membersData || [];
  const manageMembersForm = document.getElementById("manage-members-form");
  const saveButton = manageMembersForm.querySelector(".js-save-button");
  const roleCheckboxes = Array.prototype.slice.call(
    document.querySelectorAll(".js-role-checkbox")
  );

  const newData = membersData.map(function (data) {
    return Object.assign({}, data);
  });

  roleCheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function (e) {
      const target = e.target;
      const role = e.target.name;

      const member = newData.find(function (data) {
        return data.email === target.dataset.memberEmail;
      });

      const originalMember = membersData.find(function (data) {
        return data.email === target.dataset.memberEmail;
      });

      if (checkbox.checked && !member.roles.includes(role)) {
        member.roles = member.roles.concat(role);
      }

      if (!checkbox.checked && member.roles.includes(role)) {
        member.roles = member.roles.filter(function (data) {
          return data !== role;
        });
      }

      if (
        JSON.stringify(member.roles.sort()) !==
        JSON.stringify(originalMember.roles.sort())
      ) {
        member.dirty = true;
      } else {
        member.dirty = false;
      }

      const dirtyState = newData.filter(function (data) {
        return data.dirty;
      });

      saveButton.disabled = !dirtyState.length;
    });
  });

  manageMembersForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const form = e.target;
    const membersField = manageMembersForm.querySelector("#members");
    const dirtyData = newData.filter(function (data) {
      return data.dirty;
    });

    membersField.value = JSON.stringify(
      dirtyData.map(function (data) {
        return {
          email: data.email,
          roles: data.roles,
        };
      })
    );

    form.submit();
  });
}

export { inviteMember, updateMembers };
