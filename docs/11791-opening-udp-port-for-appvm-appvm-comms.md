Hello, I was trying to bind a UDP port from rust code via 
```
fn main() -> std::io::Result<()>
{
    let socket = UdpSocket::bind("10:137:0:14:666")?;
```
but I was getting "Error: Custom { kind: Uncategorized, error: "failed to lookup address information: Name or service not known" }"

Is there a quick way to allow this without reading too many documents? current threat model is low.