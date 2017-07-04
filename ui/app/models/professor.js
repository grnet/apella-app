import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import professorFields from 'ui/mixins/professor';
import {VerifiedUserMixin} from 'ui/lib/common';


export default User.extend(professorFields, VerifiedUserMixin, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
