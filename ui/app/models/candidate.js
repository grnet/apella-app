import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import candidateFields from 'ui/mixins/candidate';
import {VerifiedUserMixin} from 'ui/lib/common';


export default User.extend(candidateFields, VerifiedUserMixin, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
