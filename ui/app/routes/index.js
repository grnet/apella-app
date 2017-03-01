import Ember from 'ember';

const {
  get
} = Ember;

const ROLE_ROUTE_MAP = {
  'professor': 'positions-latest.index',
  'candidate': 'positions-latest.index',
}

const DEFAULT_ROUTE = 'auth.profile';

export default Ember.Route.extend({
  session: Ember.inject.service(),
  beforeModel(transition) {
    if (get(this, 'session.isAuthenticated')) {
      let role = get(this, 'session.session.authenticated.role');
      transition.abort();
      let set_academic = get(this, 'session.session.authenticated.can_set_academic');
      if (set_academic) { return this.transitionTo('auth.profile'); }
      return this.transitionTo(ROLE_ROUTE_MAP[role] || DEFAULT_ROUTE);
    }
  }
});
