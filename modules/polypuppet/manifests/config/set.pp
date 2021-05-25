define polypuppet::config::set (
  $value,
) {

  exec { "polypuppet config ${title}":
    command => "polypuppet config ${title} ${value}",
    unless  => "polypuppet test config ${title} ${value}",
    path    => $::path,
  }

}
