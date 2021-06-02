class polypuppet::config::role(
  $building  = $polypuppet::building,
  $classroom = $polypuppet::classroom,
  $token     = $polypuppet::token,
) {

  if $classroom != undef and $building != undef and $token != undef {
    $hidden_command = Sensitive("polypuppet login classroom ${building} ${classroom} ${token}")
    exec { 'setup classroom':
      command => $hidden_command,
      path    => $::path,
      unless  => "polypuppet test classroom ${building} ${classroom}",
    }
  }

}
