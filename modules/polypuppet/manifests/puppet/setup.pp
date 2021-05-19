class polypuppet::puppet::setup (
  $role = $polypuppet::puppet_role,
) {

  case $role {
    'agent': { contain polypuppet::puppet::agent }
    'server': { contain polypuppet::puppet::server }
    default: {
      err('Wrong puppet_role')
    }
  }

}
