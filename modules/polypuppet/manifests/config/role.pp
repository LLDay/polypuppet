class polypuppet::config::role(
  $audience = $polypuppet::audience,
  $token = $polypuppet::token,
) {

  if $audience != undef and $token != undef {
    $hidden_command = Sensitive("polypuppet login audience ${audience} ${token}")
    exec { 'setup audience number':
      command => $hidden_command,
      path    => $::path,
      unless  => "polypuppet test config audience ${audience}",
    }
  }

}
