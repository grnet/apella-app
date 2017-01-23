import Ember from 'ember';

function isHelpdesk(role) {
  return role === 'helpdeskadmin' || role === 'helpdeskuser';
}

function call_utils(route, model) {
  let messages = get(route, 'messageService');
  let adapter = get(route, 'store').adapterFor(get(model, 'role'));
  let url = adapter.buildURL(get(model, 'role'), get(model, 'id'), 'findRecord');
  let token = get(route, 'user.auth_token');
  return [url, token, messages]
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
  label: 'verifyUser',
  icon: 'done',
  action(route, model) {
    model.set('is_active', true);
    model.set('is_verified', true);
    model.set('is_rejected', false);
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
  hidden: computed('model.is_verified', 'model.is_rejected',  'model.verification_pending', 'role',  function(){
    if (!isHelpdesk(get(this, 'role')))  return true
    if (get(this, 'model.is_verified')) return true
    if (get(this, 'model.is_rejected')) return false;
    return !(get(this, 'model.verification_pending'));
  }),
  confirm: true,
  prompt: {
    ok: 'verify',
    cancel: 'cancel',
    message: 'prompt.verifyUser.message',
    title: 'prompt.verifyUser.title',
  }
};

const rejectUser = {
  label: 'rejectUser',
  icon: 'clear',
  action(route, model) {
    model.set('is_verified', false);
    model.set('is_rejected', true);
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
  hidden: computed('model.is_rejected', 'model.is_verified', 'model.verification_pending', 'role', function(){
    if (!isHelpdesk(get(this, 'role')))  return true
    if (get(this, 'model.is_rejected')) return true;
    if (get(this, 'model.is_verified')) return false;
    return !(get(this, 'model.verification_pending'));
  }),
  confirm: true,
  prompt: {
    ok: 'reject',
    cancel: 'cancel',
    message: 'prompt.rejectUser.message',
    title: 'prompt.rejectUser.title',
  }
};

const requestProfileChanges = {
  label: 'request.profile.changes',
  primary: true,
  text: true,
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


export { goToDetails, applyCandidacy, cancelPosition,
  cancelCandidacy, goToPosition,
  rejectUser, verifyUser,
  requestProfileChanges,
  deactivateUser, activateUser};

