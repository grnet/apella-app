import User from 'ui/models/user';
import {normalizeUser, serializeUser, normalizeUserErrors} from 'ui/utils/common/users';
import professorFields from 'ui/mixins/professor';


export default User.extend(professorFields, {
  __api__: {
    normalizeErrors: normalizeUserErrors,
    normalize: normalizeUser,
    serialize: serializeUser
  },
});
