import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import institutionManagerFields from 'ui/mixins/institution-manager';
import {VerifiedUserMixin} from 'ui/lib/common';

export default User.extend(institutionManagerFields, VerifiedUserMixin, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
