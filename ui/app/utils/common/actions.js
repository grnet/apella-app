import Ember from 'ember';

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
  hidden: computed('model.is_active', 'model.email_verified', function(){
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
  hidden: computed('model.is_active', 'model.email_verified', function(){
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
    model.set('verification_pending', false);
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
  hidden: computed('model.is_rejected', 'model.verification_pending', function(){
    return !(get(this, 'model.is_rejected') || get(this, 'model.verification_pending'));
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
    model.set('verification_pending', false);
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
  hidden: computed('model.is_verified', 'model.verification_pending', function(){
    return !(get(this, 'model.is_verified') || get(this, 'model.verification_pending'));
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
  label: 'requestProfileChanges',
  icon: 'compare_arrows',
  action(route, model) {
    model.set('verification_pending', false);
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
  hidden: computed.not('model.verification_pending'),
  confirm: true,
  prompt: {
    ok: 'requestChanages',
    cancel: 'cancel',
    message: 'prompt.requestProfileChanges.message',
    title: 'prompt.requestProfileChanges.title',
  }
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

