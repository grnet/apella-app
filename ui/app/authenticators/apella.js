import Ember from 'ember';
import ApimasAuthenticator from 'ember-gen-apimas/authenticators/apimas';
import {FILE_FIELDS} from 'ui/utils/common/users';

const {
  merge, computed, get, set, inject
} = Ember;

export default ApimasAuthenticator.extend({
  processProfileData(data, profile) {
    let user = profile.user;
    user.user_id = user.id.toString();
    delete user.id;
    delete profile.user;
    if (profile.departments && profile.departments.length) {
      profile.departments.forEach((dep, i) => {
        profile.departments[i] = dep.split('/').slice(-2)[0];
      });
    }
    merge(data, user);
    merge(data, profile);

    // pick just the attributes which are used for session handling
    let SESSION_FIELDS = [
      'auth_token',
      'user_id',
      'username',
      'role',
      'institution',
      'departments',
      'rank',
      'is_foreign',
      'is_secretary',
      'can_set_academic',
      'id',
      'pending_role',
      'is_verified',
      'login_method',
      'email',
      'has_accepted_terms',
      'can_create_positions',
      'can_create_registries'
    ];

    let cleaned = {}
    for (let key of SESSION_FIELDS) {
      if (data.hasOwnProperty(key)) {
        cleaned[key] = data[key];
      }
    }
    data = cleaned;

    if (data.id) {
      data.id = data.id.toString();
    }

    // process unverified users as no-role users
    if (data.hasOwnProperty('is_verified') && data.is_verified === false) {
      data.pending_role = data.role;
      data.role = 'unverified-user';
    }
    if (data.login_method === 'academic') {
      data.username = data.email;
    }

    if (data.can_set_academic) {
      let gen = get(this, 'gen');
      gen.get('gens').forEach((gen) => {
        let name = get(gen, 'routeName');
        if (!name.startsWith('auth') && !name.includes('jira-issue')) {
          set(gen, 'hasPermission', false);
          set(gen, 'menuDisplay', false);
        }
      });
    }
    return data;
  }
})
