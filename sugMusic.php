<?php
include("includes/includedFiles.php");
?>





<div class="playlistsContainer">

	<div class="gridViewContainer">
		<h2>Recommended Playlist</h2>

			<?php

				$fh = fopen('output.txt','r');
				$line = fgets($fh);
			fclose($fh);

			$playlistsQuery = mysqli_query($con, "SELECT * FROM playlists WHERE owner='$line'");


			while($row = mysqli_fetch_array($playlistsQuery)) {

				$playlist = new Playlist($con, $row);

				echo "<div class='gridViewItem' role='link' tabindex='0' 
							onclick='openPage(\"playlist.php?id=" . $playlist->getId() . "\")'>

						<div class='playlistImage'>
							<img src='assets/images/icons/playlist.png'>
						</div>
						
						<div class='gridViewInfo'>"
							. $playlist->getName() .
						"</div>

					</div>";



			}
			?>	







	</div>
</div>