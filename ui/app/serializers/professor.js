import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    cv_professor: embedded,
    cv: embedded,
    diplomas: embedded,
    publications: embedded,
  }
});
