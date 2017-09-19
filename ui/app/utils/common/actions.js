import Ember from 'ember';
import fetch from "ember-network/fetch";

function isHelpdesk(role) {
  return role === 'helpdeskadmin' || role === 'helpdeskuser';
}

function call_utils(route, model) {
  let messages = get(route, 'messageService');
  let role = get(model, 'role');
  if ( role === 'institutionmanager') {
    role = 'institution-manager';
  }
  let adapter = get(route, 'store').adapterFor(role);
  let url = adapter.buildURL(role, get(model, 'id'), 'findRecord');
  let token = get(route, 'user.auth_token');
  return [url, token, messages];
}

function application_utils(route, model) {
  let messages = get(route, 'messageService');
  let token = get(route, 'user.auth_token');
  let adapter = route.store.adapterFor('user-application');
  let url = adapter.buildURL('user-application', get(model, 'id'), 'findRecord');
  return [url, token, messages];
}

function managerVerifies(role, model_role) {
  return role === 'institutionmanager' && model_role === 'assistant';
}

const {
  computed,
  get,
} = Ember;

// Common
function  goToDetails(type, hidden, calc, calc_params) {
  return {
    label: 'details.label',
    icon: 'remove red eye',
     hidden: computed('model.othersCanView', function() {
      if(type === 'position_history' && calc) {
        let row_id = get(this, 'model.id'),
          position_id = calc_params;
        if(row_id === position_id) {
          hidden = true;
        }
        else {
          hidden = false;
        }
      }
      return hidden;
     }),

     args: computed('model', function() {
       let model = get(this, 'model');
       let res = model.get('_internalModel.modelName');
       return [`${res}.record.index`, model];
     }),
     action: 'goTo'
  };
}

// Position

const applyCandidacy = {
  label: 'applyCandidacy',
  icon: 'person_add',
  classNames: 'md-icon-success',
  permissions: [{'resource': 'candidacies', 'action': 'create'}],
  hidden: computed('model.is_open', 'role', 'model.can_apply', 'model.applicant', 'model.position_type', function(){
    let is_helpdeskadmin = get(this, 'role') === 'helpdeskadmin';
    if (is_helpdeskadmin)  { return false; }

    // If the position is of type 'renewal' or 'tenure' and the logged in user
    // is not the position's applicant hide applyCandidacy action
    let user_id = get(this, 'session.session.authenticated.user_id');
    let applicant_id = get(this, 'model.applicant.id');
    let is_election = get(this, 'model.position_type') === 'election';
    if (!is_election && (applicant_id != user_id)) { return true; }


    return !get(this, 'model.is_open') || !get(this, 'model.can_apply');
  }),
  action(route, model){
    let id = get(model, 'id');
    route.transitionTo('candidacy.create', { queryParams: { position: id }});
  }
};

const cancelPosition = {
  label: 'cancelPosition',
  icon: 'highlight_off',
  accent: true,
  action(route, model) {
    model.set('state', 'cancelled');
    let m = route.get('messageService');
    let promises = [
      get(model, 'subject'),
      get(model, 'subject_area')
    ];
    return Ember.RSVP.all(promises).then((res) => {
      model.save().then((value) => {
        m.setSuccess('form.saved');
        return value;
      }, (reason) => {
        model.rollbackAttributes();
        m.setError('reason.errors');
        return reason.errors;
      });
    });
  },
  permissions: [{action: 'edit'}],
  hidden: computed('model.is_posted', 'role', function(){
    if (get(this, 'role') === 'helpdeskadmin') { return false;}
    return !get(this, 'model.is_posted');
  }),
  confirm: true,
  prompt: {
    ok: 'cancelPosition',
    cancel: 'cancel',
    message: 'prompt.cancelPosition.message',
    title: 'prompt.cancelPosition.title',
  }
};

const setElecting = {
  label: 'setElecting',
  icon: 'people_outline',
  accent: true,
  action(route, model) {
    model.set('state', 'electing');
    let m = route.get('messageService');
    model.save().then((value) => {
      m.setSuccess('form.saved');
      return value;
    }, (reason) => {
      model.rollbackAttributes();
      m.setError('reason.errors');
      return reason.errors;
    });
  },
  permissions: [{action: 'edit'}],
  hidden: computed('model.state', 'model.is_closed', function(){
    return !(get(this, 'model.is_closed') || get(this, 'model.state') === 'revoked');
  }),
  confirm: true,
  prompt: {
    ok: 'ok',
    cancel: 'cancel',
    message: 'prompt.setElecting.message',
    title: 'prompt.setElecting.title',
  }
};

const setRevoked = {
  label: 'setRevoked',
  icon: 'autorenew',
  accent: true,
  action(route, model) {
    model.set('state', 'revoked');
    let m = route.get('messageService');
    model.save().then((value) => {
      m.setSuccess('form.saved');
      return value;
    }, (reason) => {
      model.rollbackAttributes();
      m.setError('reason.errors');
      return reason.errors;
    });
  },
  permissions: [{action: 'edit'}],
  hidden: computed('model.revocation_decision', 'model.state', function(){
    let file = get(this, 'model.revocation_decision');
    return !(file && file.content && get(this, 'model.state') === 'electing');
  }),
  confirm: true,
  prompt: {
    ok: 'ok',
    cancel: 'cancel',
    message: 'prompt.setRevoked.message',
    title: 'prompt.setRevoked.title',
  }
};

const setFailed = {
  label: 'setFailed',
  icon: 'warning',
  accent: true,
  action(route, model) {
    model.set('state', 'failed');
    let m = route.get('messageService');
    model.save().then((value) => {
      m.setSuccess('form.saved');
      return value;
    }, (reason) => {
      model.rollbackAttributes();
      m.setError('reason.errors');
      return reason.errors;
    });
  },
  permissions: [{action: 'edit'}],
  hidden: computed('model.failed_election_decision', 'model.state', function(){
    let file = get(this, 'model.failed_election_decision');
    return !(file && file.content && get(this, 'model.state') === 'electing');
  }),
  confirm: true,
  prompt: {
    ok: 'ok',
    cancel: 'cancel',
    message: 'prompt.setFailed.message',
    title: 'prompt.setFailed.title',
  }
};

const setSuccessful = {
  label: 'setSuccessful',
  icon: 'person',
  accent: true,
  action(route, model) {
    model.set('state', 'successful');
    let m = route.get('messageService');
    model.save().then((value) => {
      m.setSuccess('form.saved');
      return value;
    }, (reason) => {
      model.rollbackAttributes();
      m.setError('reason.errors');
      return reason.errors;
    });
  },
  permissions: [{action: 'edit'}],
  hidden: computed('model.nomination_act', 'model.nomination_act_fek', 'model.state', function(){
    let file = get(this, 'model.nomination_act');
    let fek = get(this, 'model.nomination_act_fek');
    return !(file && file.content && fek && get(this, 'model.state') === 'electing');
  }),
  confirm: true,
  prompt: {
    ok: 'ok',
    cancel: 'cancel',
    message: 'prompt.setSuccessful.message',
    title: 'prompt.setSuccessful.title',
  }
};

// Candidacy

const cancelCandidacy = {
  label: 'withdrawal',
  icon: 'delete forever',
  accent: true,
  action(route, model) {
    return model.get('candidate').then(() => {
      model.set('state', 'cancelled');
      let m = route.get('messageService');
      return model.save().then((value) => {
        m.setSuccess('form.saved');
        return value;
      }, (reason) => {
        model.rollbackAttributes();
        m.setError('reason.errors');
        return reason;
      });
    });
  },
  hidden: computed('model.state', 'model.position.is_open', 'model.position.is_closed', 'model.position.state', 'model.candidate.id', 'model.position.electors_meeting_date', function() {

    let candidacy_cancelled = get(this, 'model.state') === 'cancelled';
    if (candidacy_cancelled) { return true; }

    let role = get(this, 'session.session.authenticated.role');
    let user_id = get(this, 'session.session.authenticated.user_id');
    let position_open = get(this, 'model.position.is_open');
    let position_closed = get(this, 'model.position.is_closed');
    let position_electing = get(this, 'model.position.state') === 'electing';
    let is_helpdeskadmin = role === 'helpdeskadmin';
    let is_candidate = user_id === get(this, 'model.candidate.id');
    let electors_at = get(this, 'model.position_closed.electors_meeting_date');
    let before_deadline = true;
    if (electors_at) {
      before_deadline =  moment().isBefore(electors_at);
    }

    if (is_helpdeskadmin && (position_closed || position_electing) && before_deadline) { return false; }
    if (is_candidate && (position_open || position_closed)) { return false; }

    return true;

  }),
  confirm: true,
  prompt: computed('model.position.is_open', function(){
    let role = get(this, 'session.session.authenticated.role');
    let position_open = get(this, 'model.position.is_open');
    let is_helpdeskadmin = role === 'helpdeskadmin';
    let message = 'prompt.withdrawal_helpdesk.message';
    let noControls = true;

    if (is_helpdeskadmin || position_open ) {
      message = 'prompt.withdrawal.message';
      noControls = false;
    }

    return {
      ok: 'withdrawal',
      cancel: 'cancel',
      title: 'prompt.withdrawal.title',
      noControls: noControls,
      message: message
    };
  })
};

const deactivateUser = {
  label: 'deactivateUser',
  icon: 'cancel',
  accent: true,
  action(route, model) {
    model.set('is_active', false);
    let m = route.get('messageService');
    return model.save().then((value) => {
      m.setSuccess('form.saved');
      return value;
    }, (reason) => {
      model.rollbackAttributes();
      m.setError('reason.errors');
      return reason;
    });
  },
  hidden: computed('model.is_active', 'model.email_verified', 'role', function(){
    if (!isHelpdesk(get(this, 'role'))) { return true; }
    return !get(this, 'model.is_active') || !get(this, 'model.email_verified');
  }),
  confirm: true,
  prompt: {
    ok: 'deactivate',
    cancel: 'cancel',
    message: 'prompt.deactivateUser.message',
    title: 'prompt.deactivateUser.title',
  }
};

const activateUser = {
  label: 'activateUser',
  icon: 'check_circle',
  classNames: 'md-icon-success',
  action(route, model) {
    model.set('is_active', true);
    let m = route.get('messageService');
    return model.save().then((value) => {
      m.setSuccess('form.saved');
      return value;
    }, (reason) => {
      model.rollbackAttributes();
      m.setError('reason.errors');
      return reason;
    });
  },
  hidden: computed('model.is_active', 'model.email_verified', 'role', function(){
    if (!isHelpdesk(get(this, 'role'))) { return true; }
    return get(this, 'model.is_active') || !get(this, 'model.email_verified');
  }),
  confirm: true,
  prompt: {
    ok: 'activate',
    cancel: 'cancel',
    message: 'prompt.activateUser.message',
    title: 'prompt.activateUser.title',
  }
};

const createIssue = {
  label: 'createIssue',
  icon: 'mail_outline',
  hidden: computed('role', function(){
    return !get(this, 'role').startsWith('helpdesk');
  }),
  action(route, model){
    let id = get(model, 'user_id');
    route.transitionTo('jira-issue.create', { queryParams: { user_id: id }});
  }
};

const verifyUser = {
  label: 'verify.user',
  icon: 'check_circle',
  classNames: 'md-icon-success',
  action: function(route, model) {
    let [url, token, messages] = call_utils(route, model);
    return fetch(url + 'verify_user/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('verify.user.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('verify.user.error');
    });
  },
  confirm: true,
  prompt: {
    ok: 'submit',
    cancel: 'cancel',
    message: 'verify.user.message',
    title: 'verify.user.title',
  },
  hidden: computed('model.verification_pending', 'model.is_verified', 'model.is_rejected', 'role', 'model.role', function() {
    let verified = get(this, 'model.is_verified');
    let rejected = get(this, 'model.is_rejected');
    let pending = get(this, 'model.verification_pending');
    let role = get(this, 'role');
    let model_role = get(this, 'model.role');
    if (managerVerifies(role, model_role)) { return verified; }
    if (isHelpdesk(role)) { return !(rejected  || (!verified && pending)); }
    return true;
  }),
};

const rejectUser = {
  label: 'reject.user',
  icon: 'cancel',
  accent: true,
  action: function(route, model) {
    let [url, token, messages] = call_utils(route, model);
    return fetch(url + 'reject_user/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('reject.user.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('reject.user..error');
    });
  },
  hidden: computed('model.is_rejected', 'model.is_verified', 'model.verification_pending', 'role', 'model.role', function(){
    let verified = get(this, 'model.is_verified');
    let rejected = get(this, 'model.is_rejected');
    let pending = get(this, 'model.verification_pending');
    let role = get(this, 'role');
    let model_role = get(this, 'model.role');
    if (managerVerifies(role, model_role)) { return rejected; }
    if (isHelpdesk(role)) { return !(verified  || (!rejected && pending)); }
    return true;
  }),
  confirm: true,
  prompt: {
    ok: 'submit',
    cancel: 'cancel',
    message: 'reject.user.message',
    title: 'reject.user.title',
  }
};

const requestProfileChanges = {
  label: 'request.profile.changes',
  primary: true,
  icon: 'sync_problem',
  action: function(route, model) {
    let [url, token, messages] = call_utils(route, model);
    return fetch(url + 'request_changes/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('request.changes.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('request.changes.error');
    });
  },
  confirm: true,
  prompt: {
    title: 'request.profile.changes',
    message: 'request.profile.changes.message',
    ok: 'submit',
    cancel: 'cancel'
  },
  hidden: computed('model.verification_pending', 'model.is_verified', 'model.is_rejected', 'role', function() {
    let verified = get(this, 'model.is_verified');
    let rejected = get(this, 'model.is_rejected');
    let pending = get(this, 'model.verification_pending');
    let role = get(this, 'role');
    if (isHelpdesk(role)) { return !(!verified  && !rejected && pending); }
    return true;
  }),
};

const  goToPosition = {
  label: 'position_details.label',
  icon: 'event_available',
  action(route, model) {
    let position_id = get(this, 'model.position.id') || get(this, 'model.position_id');
    route.transitionTo('position.record.index', position_id);
  },
  hidden: computed('model.position_id', 'model.position.id', function(){
    if (get(this, 'model.position_id') > 0 || get(this, 'model.position.id')) {
      return false;
    }
    return true;
  })
};

const change_password = {
  raised: false,
  label: 'password.change',
  confirm: true,
  action: function() {},
  hidden: computed('model.login_method', function() {
    return get(this, 'model.login_method') !== 'password';
  }),
  prompt: {
    title: 'password.change.title',
    contentComponent: 'change-password',
    noControls: true
  }
};

// Applications

const acceptApplication = {
  label: 'accept_application',
  icon: 'check_circle',
  classNames: 'md-icon-success',
  action: function(route, model) {
    let [url, token, messages] = application_utils(route, model);
    return fetch(url + 'accept_application/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('user_application.accept.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('user_application.accept.error');
    });
  },
  confirm: true,
  prompt: {
    ok: 'submit',
    cancel: 'cancel',
    message: 'user_application.accept_application.message',
    title: 'user_application.prompt.title',
  },
  hidden: computed('role', 'model.state', 'model.position_id', function(){
    let role = get(this, 'role'),
        state = get(this, 'model.state'),
        has_position = get(this, 'model.position_id') > 0;
    let manager_or_assistant = (role === 'institutionmanager' || role === 'assistant');
    if (!manager_or_assistant) { return true; }
    if (state === 'approved')  { return true; }
    if (has_position) { return true; }
  }),

};

const rejectApplication = {
  label: 'reject_application',
  icon: 'cancel',
  accent: true,
  action: function(route, model) {
    let [url, token, messages] = application_utils(route, model);
    return fetch(url + 'reject_application/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Token ${token}`
      },
    }).then((resp) => {
      if (resp.status === 200) {
        model.reload().then(() => {
          messages.setSuccess('user_application.reject.success');
        });
      } else {
        throw new Error('error');
      }
    }).catch((err) => {
      messages.setError('user_application.reject.error');
    });
  },
  confirm: true,
  prompt: {
    ok: 'submit',
    cancel: 'cancel',
    message: 'user_application.reject_application.message',
    title: 'user_application.prompt.title',
  },
  hidden: computed('role', 'model.state', 'model.position_id', function(){
    let role = get(this, 'role'),
        state = get(this, 'model.state'),
        has_position = get(this, 'model.position_id') > 0;
    let manager_or_assistant = (role === 'institutionmanager' || role === 'assistant');
    if (!manager_or_assistant) { return true; }
    if (state === 'rejected')  { return true; }
    if (has_position) { return true; }
  }),
};

const  goToProfessor = {
  label: 'professor.profile.label',
  icon: 'portrait',
  action(route, model) {
    let id = get(this, 'model.user.id');
    route.store.queryRecord('professor', {user_id: id}).then((professor) => {
      route.transitionTo('professor.record.index', professor.id);
    });
  },
  hidden: computed('role', function(){
    let professor = get(this, 'role') === 'professor';
    if (professor) { return true; }
  })
};

const createPosition = {
  label: 'createPosition',
  icon: 'add',
  permissions: [{'resource': 'positions', 'action': 'create'}],
  hidden: computed('model.state', 'model.position_id', 'model.position_state', function(){
    let state = get(this, 'model.state'),
      position_state = get(this, 'model.position_state'),
      has_position = get(this, 'model.position_id') > 0;
    return !(state === 'approved') || (has_position && position_state !== 'cancelled');
  }),
  action(route, model){
    let id = get(model, 'id');
    route.transitionTo('position.create', { queryParams: { application: id }});
  }
};

const applyApplicationCandidacy = {
  label: 'applyCandidacy',
  icon: 'person_add',
  classNames: 'md-icon-success',
  permissions: [{'resource': 'candidacies', 'action': 'create'}],
  hidden: computed('model.can_accept_candidacies', 'role', 'model.position_state', function(){
    let role = get(this, 'role');
    let candidate = role === 'professor' || role === 'candidate';
    let can_apply = get(this, 'model.can_accept_candidacies');
    let position_state = get(this, 'model.position_state');
    return !(candidate && can_apply) || position_state === 'cancelled';
  }),
  action(route, model){
    let id = get(model, 'position_id');
    route.transitionTo('candidacy.create', { queryParams: { position: id }});
  }
};

function exportCSV(route, model, modelName) {
  let token = get(route, 'user.auth_token');
  let adapter = get(route, 'store').adapterFor(modelName);
  let url = adapter.buildURL(modelName)+ 'report/';
  let m = get(route, 'messageService')
  return fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Token ${token}`,
    }
  }).then((resp) => {
    if (resp.status < 200 || resp.status > 299) {
      throw resp;
    }
    let a = $("<a style='display: none;'/>");
    let url = window.URL.createObjectURL(resp._bodyBlob);
    let name = `${modelName}_${moment().format('DD/MM/YYYY_HH:mm')}.csv`;
    a.attr("href", url);
    a.attr("download", name);
    $("body").append(a);
    a[0].click();
    window.URL.revokeObjectURL(url);
    a.remove();
  }).catch((err) => {
    m.setError('reason.errors');
    throw err;
  }).finally(() => {
  });
}

const exportProf = {
  label: 'exportCSV',
  icon: 'file_download',
  hidden: computed('role', function(){
    let role = get(this, 'role');
    return !(role === 'helpdeskadmin' || role === 'assistant' || role === 'institutionmanager');
  }),
  action: function(route, model) {
    return exportCSV(route, model, 'professor');
  },
};

const exportPositions = {
  label: 'exportCSV',
  icon: 'file_download',
  hidden: computed('role', function(){
    let role = get(this, 'role');
    return role === 'professor' || role === 'candidate'
  }),
  action: function(route, model) {
    return exportCSV(route, model, 'position');
  },
};

const exportRegistries = {
  label: 'exportCSV',
  icon: 'file_download',
  hidden: computed('role', function(){
    let role = get(this, 'role');
    return role === 'professor' || role === 'candidate'
  }),
  action: function(route, model) {
    return exportCSV(route, model, 'registry', 'registries');
  },
};


let positionActions = {
  cancelPosition: cancelPosition,
  setElecting: setElecting,
  setRevoked: setRevoked,
  setFailed: setFailed,
  setSuccessful: setSuccessful
};

let applicationActions = {
  rejectApplication: rejectApplication,
  acceptApplication: acceptApplication,
  goToProfessor: goToProfessor,
  createPosition: createPosition,
  applyApplicationCandidacy: applyApplicationCandidacy
};

export { goToDetails, applyCandidacy,
  cancelCandidacy, goToPosition,
  rejectUser, verifyUser,
  requestProfileChanges,
  deactivateUser, activateUser,
  createIssue,
  change_password,
  isHelpdesk,
  positionActions,
  applicationActions,
  exportProf,
  exportPositions,
  exportRegistries,
};

