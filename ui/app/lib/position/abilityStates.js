const {
  computed,
  get
} = Ember;

let abilityStates = {
  is_latest: computed('model.is_latest', function(){
     return get(this, 'model.is_latest');
  }),
  can_create: computed('user.can_create_positions', 'role', function() {
    let role = get(this, 'role');
    let can_create = get(this, 'user.can_create_positions');
    if (role === 'assistant') {
      return can_create;
    }
    return true;
  }),
  'open': computed('model.state', 'model.ends_at', 'is_latest',  function() {
    return get(this, 'model.state') === 'open' &&
      moment(get(this, 'model.ends_at')).isBefore(new Date()) &&
      get(this, 'is_latest');
  }),
  electing: computed('state', 'can_create', 'is_latest', function() {
    return get(this, 'model.state') === 'electing' &&
      get(this, 'is_latest') &&
      get(this, 'can_create');
  }),
  before_open: computed('model.is_posted', 'is_latest', 'can_create', function(){
    return get(this, 'model.is_posted') &&
      get(this, 'is_latest') &&
      get(this, 'can_create');
  }),
  after_closed: computed('model.is_closed', 'is_latest', 'can_create', function(){
    return get(this, 'model.is_closed') &&
      get(this, 'is_latest') &&
      get(this, 'can_create');
  }),
  revoked: computed('model.state', 'is_latest', 'can_create', function(){
    return get(this, 'model.state') === 'revoked' &&
      get(this, 'is_latest') &&
      get(this, 'can_create');
  }),
  owned: computed('model.author.user_id', 'user.user_id', 'role',  function() {
    let is_author = this.get('model.author.user_id') == get(this, 'user.user_id');
    let is_manager = get(this, 'role') == 'institutionmanager';
    return is_manager || is_author;
  }),
  owned_by_assistant: computed('role', 'user.can_create_positions', 'is_latest', function(){
    let is_assistant = get(this, 'role') == 'assistant';
    let can_create = get(this, 'user.can_create_positions');
    let is_latest = get(this, 'is_latest');
    return is_assistant && can_create && is_latest;
  })
}

export {abilityStates};
