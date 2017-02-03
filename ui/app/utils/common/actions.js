import Ember from 'ember';
import fetch from "ember-network/fetch";

function isHelpdesk(role) {
  return role === 'helpdeskadmin' || role === 'helpdeskuser';
}

function call_utils(route, model) {
  let messages = get(route, 'messageService');
  let role = get(model, 'role');
  if ( role == 'institutionmanager') {
    role = 'institution-manager';
  }
  let adapter = get(route, 'store').adapterFor(role);
  let url = adapter.buildURL(role, get(model, 'id'), 'findRecord');
  let token = get(route, 'user.auth_token');
  return [url, token, messages]
}

function managerVerifies(role, model_role) {
  return role == 'institutionmanager' && model_role == 'assistant'
}

const {
  computed,
  get,
  merge, assign
} = Ember;

// Common

const  goToDetails = {
  label: 'details.label',
  icon: 'remove red eye',
  action(route, model, aaa) {
    // TMP
    let resource = model.get('_internalModel.modelName'),
      dest_route = `${resource}.record.index`;
    route.transitionTo(dest_route, model);
  }
};

// Position

const applyCandidacy = {
  label: 'applyCandidacy',
  icon: 'person_add',
  permissions: [{'resource': 'candidacies', 'action': 'create'}],
  hidden: computed('model.is_open', 'role', 'model.can_apply', function(){
    let role = get(this, 'role');
    let is_helpdeskadmin = get(this, 'role') == 'helpdeskadmin';
    if (is_helpdeskadmin)  return false;
    return !get(this, 'model.is_open') || !get(this, 'model.can_apply')
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
    let m = route.get('messageService')
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
  hidden: computed('model.code', 'model.state', function(){
    let starts_at = get(get(this, 'model'), 'starts_at')
    let state = get(get(this, 'model'), 'state');
    let before_open = moment(new Date()).isBefore(moment(starts_at));
    return !(before_open && (state == 'posted'))
  }),
  confirm: true,
  prompt: {
    ok: 'cancelPosition',
    cancel: 'cancel',
    message: 'prompt.cancelPosition.message',
    title: 'prompt.cancelPosition.title',
  }
};

// Candidacy

const cancelCandidacy = {
  label: 'withdrawal',
  icon: 'delete forever',
  accent: true,
  permissions: [{action: 'edit'}],
  action(route, model) {
    return model.get('candidate').then(() => {
      model.set('state', 'cancelled');
      let m = route.get('messageService')
      return model.save().then((value) => {
        m.setSuccess('form.saved');
        return value;
      }, (reason) => {
        model.rollbackAttributes();
        m.setError('reason.errors');
        return reason;
      });
    })
  },
  hidden: computed('model.state', function(){
    return get(this, 'model.state') === 'cancelled';
  }),
  confirm: true,
  prompt: {
    ok: 'withdrawal',
    cancel: 'cancel',
    message: 'prompt.withdrawal.message',
    title: 'prompt.withdrawal.title',
  }
};

const deactivateUser = {
  label: 'deactivateUser',
  icon: 'clear',
  accent: true,
  action(route, model) {
    model.set('is_active', false);
    let m = route.get('messageService')
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
    if (!isHelpdesk(get(this, 'role')))  return true
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
  icon: 'done',
  action(route, model) {
    model.set('is_active', true);
    let m = route.get('messageService')
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
    if (!isHelpdesk(get(this, 'role')))  return true
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

const verifyUser = {
  label: 'verify.user',
  icon: 'done',
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
        throw new Error(res);
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
    if (managerVerifies(role, model_role)) { return verified }
    if (isHelpdesk(role)) { return !(rejected  || (!verified && pending)); }
    return true;
  }),
};

const rejectUser = {
  label: 'reject.user',
  icon: 'clear',
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
        throw new Error(res);
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
    if (managerVerifies(role, model_role)) { return rejected }
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
  icon: 'compare_arrows',
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
        throw new Error(res);
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
    let position_id = get(this, 'model.position.id');
    route.transitionTo('position.record.index', position_id);
  }
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
}


export { goToDetails, applyCandidacy, cancelPosition,
  cancelCandidacy, goToPosition,
  rejectUser, verifyUser,
  requestProfileChanges,
  deactivateUser, activateUser,
  change_password,
  isHelpdesk,
};

