function mustAcceptTerms() {
  return (key, value) => {
    return value || 'acceptTerms.message';
  };
}

export {
  mustAcceptTerms
};

