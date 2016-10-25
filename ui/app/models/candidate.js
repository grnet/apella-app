import DS from 'ember-data';
import ENV from 'ui/config/environment';
import User from 'ui/models/user';
import {normalizeUser, serializeUser} from 'ui/utils/common/users';

const CHOICES = ENV.APP.resource_choices;

export default User.extend({
  __api__: {
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
