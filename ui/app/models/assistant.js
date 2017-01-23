import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import assistantFields from 'ui/mixins/assistant';
import {VerifiedUserMixin} from 'ui/lib/common';


export default User.extend(assistantFields, VerifiedUserMixin, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
