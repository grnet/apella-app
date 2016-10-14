/*
 * array form: [ [id_0, label_0], [id_1, label_1] ]
 * returns the label of the element with the given id or ''
 */

export default function(array, id) {

  return (array.find( (el) => { return el[0] === id; }) || [0, ''])[1];
}
