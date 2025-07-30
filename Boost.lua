local g,w,l,t,p=game,workspace,game.Lighting,workspace.Terrain,game.Players.LocalPlayer
local c=w.CurrentCamera
local u=g:GetService("RunService")
setfpscap(15)
u:Set3dRenderingEnabled(false)
l.Brightness=0
l.GlobalShadows=false
l.FogStart=0
l.FogEnd=9e9
l.Ambient=Color3.new()
l.OutdoorAmbient=Color3.new()
t.WaterWaveSize=0
t.WaterWaveSpeed=0
t.WaterReflectance=0
t.WaterTransparency=0
sethiddenproperty(t,"Decoration",false)
settings().Rendering.QualityLevel=Enum.QualityLevel.Level01
UserSettings():GetService("UserGameSettings").MasterVolume=0
pcall(function()
	c.CameraType=Enum.CameraType.Scriptable
	c.CameraSubject=nil
	c.FieldOfView=1
	local h=p.Character and p.Character:FindFirstChildOfClass("Humanoid")
	if h then h.CameraOffset=Vector3.zero h.AutoRotate=false end
end)
local function gho(v)
	pcall(function()
		if v:IsA("BasePart") then v.Transparency=1 v.CastShadow=false v.Material=Enum.Material.SmoothPlastic end
		if v:IsA("MeshPart") then v.MeshId="" v.TextureID="" end
		if v:IsA("SpecialMesh") or v:IsA("FileMesh") then v.MeshId="" v.TextureId="" end
		if v:IsA("Texture") or v:IsA("Decal") or v:IsA("SurfaceAppearance") then v:Destroy() end
		if v:IsA("Sound") then v.Volume=0 v:Stop() end
		if v:IsA("ParticleEmitter") or v:IsA("Trail") or v:IsA("Beam") then v.Enabled=false v.Lifetime=NumberRange.new(0) end
		if v:IsA("Fire") or v:IsA("Smoke") or v:IsA("Sparkles") or v:IsA("SpotLight") or v:IsA("PointLight") or v:IsA("SurfaceLight") then v.Enabled=false end
		if v:IsA("Explosion") then v.BlastPressure=1 v.BlastRadius=1 end
		if v:IsA("Constraint") then v.Visible=false end
		if v:IsA("Highlight") or v:IsA("ForceField") then v.Enabled=false end
		if v:IsA("Animator") or v:IsA("Animation") or v:IsA("AnimationTrack") or v:IsA("AnimationController") then v:Destroy() end
		if v:IsA("Shirt") or v:IsA("Pants") or v:IsA("ShirtGraphic") or v:IsA("BodyColors") or v:IsA("Accessory") then v:Destroy() end
	end)
end
for _,v in next,w:GetDescendants() do gho(v) end
for _,v in next,getnilinstances() do gho(v) for _,v2 in next,v:GetDescendants() do gho(v2) end end
w.DescendantAdded:Connect(gho)
l.ChildAdded:Connect(function(v) pcall(function() if v:IsA("PostEffect") or v:IsA("Atmosphere") then v.Enabled=false end end) end)
