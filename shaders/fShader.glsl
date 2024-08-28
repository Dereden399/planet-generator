#version 330 core

in vec2 TexCoord;

uniform ivec2 screenDimensions;
uniform float time;

out vec4 FragColor;

vec3 screenCentre = vec3(screenDimensions/2, 0);

vec3 applyLight(vec3 color, vec3 point, vec3 lightPos, vec3 viewerPos) {
  vec3 norm = normalize(point);
  vec3 toLightVector = normalize(lightPos-screenCentre-point);
  float coef = max(0.0, dot(norm, toLightVector));

  vec3 dirToViewer = normalize(viewerPos-screenCentre - point);
  vec3 halfway = normalize(dirToViewer+toLightVector);
  float spec = pow(max(dot(norm, halfway), 0.0), 32);
  
  vec3 ambient = color*0.2;
  vec3 diffuse = coef*color;
  vec3 specular = color*spec;

  return ambient + diffuse + specular;
}
void main() {
  time;
  vec3 lightPos = vec3(800, 600, 500);
  vec3 viewerPos = vec3(screenCentre.xy, 400);

  vec3 point = vec3(mix(vec2(0, 0), screenDimensions, gl_FragCoord.xy / screenDimensions),0);
  // Center the point around (screenDimensions.x / 2, screenDimensions.y / 2)
  vec3 centeredPoint = vec3(point.xy - 0.5 * screenDimensions, 0);
  float radius = min(screenDimensions.x, screenDimensions.y) * 0.25;
  vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
  
  float distanceFromCentre2 = dot(centeredPoint, centeredPoint);
  if (distanceFromCentre2 <= radius*radius) {
    color.x = 1.0;
    float z = sqrt(radius*radius - distanceFromCentre2);
    centeredPoint.z = z;
    color.xyz = applyLight(color.xyz, centeredPoint, lightPos, viewerPos);
  }

  FragColor = color;
}