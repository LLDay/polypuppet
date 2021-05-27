class polypuppet::check {
  if has_key($::facts, 'polypuppet') {

    $role = $::polypuppet['role']
    $certname = $::trusted['certname']

    if $certname =~ /^student\..*/ {
      $flow = $::polypuppet['student_flow']
      $group = $::polypuppet['student_group']
      $flow_group = $certname.match(/^student\.(\d+)\.(\d+)\..*/)

      if $role != 'student' or $flow_group[1] != $flow or $flow_group[2] != $group {
        fail("Credentials are changed explicitly. You should login again with 'polypuppet login'")
      }
    }

    if $certname =~ /^audience\..*/ {
      if $role != 'audience' {
        fail("Role is changed explicitly. You should again with 'polypuppet login'")
      }
    }

  }
}
