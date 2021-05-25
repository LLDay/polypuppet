class polypuppet::config::role(
  $building = $polypuppet::building,
  $audience = $polypuppet::audience,
  $token    = $polypuppet::token,
) {

  if $audience != undef and $building != undef and $token != undef {
    $hidden_command = Sensitive("polypuppet login audience ${building} ${audience} ${token}")
    exec { 'setup audience':
      command => $hidden_command,
      path    => $::path,
      unless  => "polypuppet test audience ${building} ${audience}",
    }
  }

}
