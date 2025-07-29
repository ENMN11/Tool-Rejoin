local g,w,l,t,p=game,workspace,game.Lighting,workspace.Terrain,game.Players.LocalPlayer
local c=w.CurrentCamera
local function s(f)pcall(f)end
l.Brightness=0
l.GlobalShadows=false
sethiddenproperty(t,"Decoration",false)
l.FogStart,l.FogEnd=0,30
t.WaterWaveSize,t.WaterWaveSpeed,t.WaterReflectance,t.WaterTransparency=0,0,0,0
settings().Rendering.QualityLevel="Level01"
UserSettings():GetService("UserGameSettings").MasterVolume=0
s(function()
	c.CameraType=Enum.CameraType.Scriptable
	c.CameraSubject=nil
	c.FieldOfView=1
	if p.Character then
		local h=p.Character:FindFirstChildOfClass("Humanoid")
		if h then h.CameraOffset=Vector3.zero h.AutoRotate=false end
	end
end)
local function gho(v)
	s(function()
		if v:IsA("BasePart")or v:IsA("Decal")or v:IsA("Texture")then v.Transparency=1 end
		if v:IsA("Sound")then v.Volume=0 v:Stop()end
		if v:IsA("ParticleEmitter")or v:IsA("Trail")or v:IsA("Beam")then v.Enabled=false v.Lifetime=NumberRange.new(0)end
		if v:IsA("Fire")or v:IsA("Smoke")or v:IsA("Sparkles")or v:IsA("SpotLight")or v:IsA("PointLight")or v:IsA("SurfaceLight")then v.Enabled=false end
		if v:IsA("Explosion")then v.BlastPressure,v.BlastRadius=1,1 end
		if v:IsA("Animator")or v:IsA("Animation")or v:IsA("AnimationTrack")or v:IsA("AnimationController")then v:Destroy()end
	end)
end
for _,v in next,w:GetDescendants()do gho(v)end
for _,v in next,getnilinstances()do gho(v)for _,v2 in next,v:GetDescendants()do gho(v2)end end
w.DescendantAdded:Connect(gho)
