import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import institutionManagerFields from 'ui/mixins/institution-manager';

const CHOICES = ENV.APP.resource_choices;

export default User.extend(institutionManagerFields, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
