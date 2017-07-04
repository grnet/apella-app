export function atLeastRank(min) {
  min = min || 1;
  return (key, value) => {
    if (value && value.length >= min ) {
      return true
    } else {
      return 'at.least.'+min+'.rank.error'
    }
  };
}
