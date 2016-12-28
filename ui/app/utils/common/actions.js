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
  icon: 'playlist add',
  permissions: [{'resource': 'candidacies', 'action': 'create'}],
  action(route, model){
    console.log(get(model, 'code'))
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

export { goToDetails, applyCandidacy, cancelPosition,
  cancelCandidacy };

