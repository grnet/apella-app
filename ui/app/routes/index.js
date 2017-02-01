import Ember from 'ember';

const {
  get
} = Ember;

const ROLE_ROUTE_MAP = {
  'professor': 'position.index',
}

const DEFAULT_ROUTE = 'auth.profile';

export default Ember.Route.extend({
  session: Ember.inject.service(),
  beforeModel(transition) {
    if (get(this, 'session.isAuthenticated')) {
      let role = get(this, 'session.session.authenticated.role');
      transition.abort();
      return this.transitionTo(ROLE_ROUTE_MAP[role] || DEFAULT_ROUTE);
    }
  }
});
