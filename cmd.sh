
#video muxer
ffmpeg -y -hide_banner -i out_zoompan.mp4 -i out.mp3 \
-vf "subtitles=output.srt:force_style='Fontname=Noto Serif SC,FontSize=24,PrimaryColour=&HAAFFCCAA'" \
-c:v libx264 -preset fast -profile:v high -shortest -map 0:v -map 1:a out_mp4/out_muxered.mp4

ffmpeg -y -hide_banner -i out_zoompan.mp4 -i out.mp3 \
-vf subtitles=output.srt:force_style='Fontname=Noto Serif SC,FontSize=24,PrimaryColour=&HAACCFFAA' \
 -c:v libx264 -preset fast -profile:v high -shortest -map 0:v -map 1:a out_mp4/out_muxered.mp4