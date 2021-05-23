class polypuppet::config::role(
  $audience = $polypuppet::polypuppet_audience,
  $token = $polypuppet::polypuppet_token,
) {

  if $audience != undef and $token != undef {
    $hidden_command = Sensitive("polypuppet audience ${audience} ${token}")
    exec { 'setup audience number':
      command => $hidden_command,
      path    => $::path,
      unless  => "polypuppet test config audience ${audience}"
    }
  }

}
