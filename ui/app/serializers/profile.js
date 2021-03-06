import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    id_passport_file: embedded,
    diplomas: embedded,
    publications: embedded,
    cv: embedded,
    cv_professor: embedded,
    leave_file: embedded,
    pubs_note: embedded,
  }
});
