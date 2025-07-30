local g,w,l,t,p=game,workspace,game.Lighting,workspace.Terrain,game.Players.LocalPlayer
local c=w.CurrentCamera
local u=game:GetService("RunService")
setfpscap(15)
u:Set3dRenderingEnabled(false)
local function s(f)pcall(f)end
l.Brightness=0
l.GlobalShadows=false
l.FogStart=0
l.FogEnd=9e9
l.Ambient=Color3.new(0,0,0)
l.OutdoorAmbient=Color3.new(0,0,0)
t.WaterWaveSize=0
t.WaterWaveSpeed=0
t.WaterReflectance=0
t.WaterTransparency=0
sethiddenproperty(t,"Decoration",false)
settings().Rendering.QualityLevel=Enum.QualityLevel.Level01
UserSettings():GetService("UserGameSettings").MasterVolume=0
for _,v in next,l:GetChildren()do if v:IsA("PostEffect")or v:IsA("Atmosphere")then s(function()v.Enabled=false end)end end
s(function()
	c.CameraType=Enum.CameraType.Scriptable
	c.CameraSubject=nil
	c.FieldOfView=1
	if p.Character then
		local h=p.Character:FindFirstChildOfClass("Humanoid")
		if h then
			h.CameraOffset=Vector3.zero
			h.AutoRotate=false
		end
	end
end)
local function gho(v)
	s(function()
		if v:IsA("BasePart")or v:IsA("Decal")or v:IsA("Texture")or v:IsA("MeshPart")or v:IsA("SpecialMesh")then v.Transparency=1 end
		if v:IsA("Sound")then v.Volume=0 v:Stop()end
		if v:IsA("ParticleEmitter")or v:IsA("Trail")or v:IsA("Beam")then v.Enabled=false v.Lifetime=NumberRange.new(0)end
		if v:IsA("Fire")or v:IsA("Smoke")or v:IsA("Sparkles")or v:IsA("SpotLight")or v:IsA("PointLight")or v:IsA("SurfaceLight")then v.Enabled=false end
		if v:IsA("ForceField")or v:IsA("Highlight")then v.Enabled=false end
		if v:IsA("Explosion")then v.BlastPressure=1 v.BlastRadius=1 end
		if v:IsA("Animator")or v:IsA("Animation")or v:IsA("AnimationTrack")or v:IsA("AnimationController")then v:Destroy()end
	end)
end
for _,v in next,w:GetDescendants()do gho(v)end
for _,v in next,getnilinstances()do gho(v)for _,v2 in next,v:GetDescendants()do gho(v2)end end
w.DescendantAdded:Connect(gho)
