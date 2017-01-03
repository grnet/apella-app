import DS from 'ember-data';
import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import {VerifiedUserMixin} from 'ui/lib/common';


export default User.extend(VerifiedUserMixin, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
